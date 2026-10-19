// Verifica a placa de vídeo Nvidia e diz o que o Studio consegue acelerar com ela nesta máquina.
// Uso: npm run gpu            (resumo em português)
//      npm run gpu -- --json  (o mesmo em JSON, lido pelo Claude no início da sessão)
// Não instala nem altera driver: só lê `nvidia-smi`, testa o encoder da placa no ffmpeg (NVENC)
// e vê se a transcrição (faster-whisper/CTranslate2) enxerga a GPU.
import {spawnSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';

// Drivers mais antigos que isto não rodam o NVENC do ffmpeg atual nem o CUDA 12 do Whisper.
export const DRIVER_MINIMO = 570;
export const LINK_DRIVER = 'https://www.nvidia.com/pt-br/drivers/';
const python = process.platform === 'win32' ? 'python' : 'python3';

const roda = (cmd, args) => spawnSync(cmd, args, {encoding: 'utf8', windowsHide: true});

export function verificarGpu() {
  const r = {nvidia: false, placa: null, driver: null, driverOk: false, nvenc: false, whisperCuda: false, bibliotecasCuda: false, link: LINK_DRIVER, minimo: DRIVER_MINIMO};

  const smi = roda('nvidia-smi', ['--query-gpu=name,driver_version', '--format=csv,noheader']);
  if (smi.status === 0 && smi.stdout.trim()) {
    const [placa, driver] = smi.stdout.trim().split('\n')[0].split(',').map((s) => s.trim());
    Object.assign(r, {nvidia: true, placa, driver, driverOk: parseFloat(driver) >= DRIVER_MINIMO});
  }
  if (!r.nvidia) return r;

  // NVENC: codifica 5 quadros pretos pela placa; só passa se driver e ffmpeg se entenderem
  const nvenc = roda('ffmpeg', ['-v', 'error', '-f', 'lavfi', '-i', 'color=c=black:s=256x256:r=30', '-frames:v', '5', '-c:v', 'h264_nvenc', '-f', 'null', '-']);
  r.nvenc = nvenc.status === 0;

  const ct2 = roda(python, ['-c', 'import ctranslate2; print(ctranslate2.get_cuda_device_count())']);
  r.whisperCuda = ct2.status === 0 && parseInt(ct2.stdout.trim(), 10) > 0;
  r.bibliotecasCuda = roda(python, ['-m', 'pip', 'show', '-q', 'nvidia-cublas-cu12', 'nvidia-cudnn-cu12']).status === 0;
  return r;
}

export function resumo(r) {
  if (!r.nvidia) return ['Sem placa Nvidia (ou sem driver): tudo roda pela CPU. Nada a fazer.'];
  const linhas = [`Placa: ${r.placa} · driver ${r.driver}`];
  linhas.push('  Remotion (desenho dos quadros): usa a placa pelo modo ANGLE, com qualquer driver.');
  linhas.push(`  Encoder da placa no ffmpeg (NVENC): ${r.nvenc ? 'funciona' : 'não funciona'}`);
  linhas.push(`  Transcrição na placa (Whisper/CUDA): ${r.whisperCuda && r.bibliotecasCuda ? 'pronta' : r.whisperCuda ? 'falta instalar as bibliotecas de CUDA (npm run instalar faz isso)' : 'não disponível'}`);
  if (!r.driverOk) {
    linhas.push('');
    linhas.push(`  >> Atualize o driver da Nvidia para a versão ${r.minimo} ou mais nova (hoje: ${r.driver}).`);
    linhas.push(`     Baixe o "NVIDIA Studio Driver" para a sua placa em ${r.link}`);
    linhas.push('     (ou pelo app NVIDIA), instale, reinicie o computador e rode "npm run instalar" de novo.');
  }
  return linhas;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const r = verificarGpu();
  if (process.argv.includes('--json')) console.log(JSON.stringify(r, null, 2));
  else console.log(resumo(r).join('\n'));
}
