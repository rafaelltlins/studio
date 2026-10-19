// Instala tudo de que o Studio precisa: dependências, transcrição local e as skills gratuitas.
// Uso: npm run instalar   (ou: node scripts/instalar.mjs)
// Cada passo é independente: se um falhar, os outros continuam e o resumo final diz o que resolver.
import {spawnSync} from 'node:child_process';
import {resumo, verificarGpu} from './verificar-gpu.mjs';

const python = process.platform === 'win32' ? 'python' : 'python3';

const passos = [
  ['Dependências do Remotion', 'npm install --no-audit --no-fund'],
  ['Transcrição local (faster-whisper)', `${python} -m pip install faster-whisper`],
  ['Recorte de figurinhas (tools/recortar_figurinha.py)', `${python} -m pip install pillow scipy numpy`],
  ['Skill remotion-best-practices', 'npx -y skills add remotion-dev/skills -s remotion-best-practices -a claude-code -y'],
  // ponytail: falha aqui costuma ser "marketplace já cadastrado"; o passo seguinte revela erro real.
  ['Marketplace da skill watch', 'claude plugin marketplace add bradautomates/claude-video', true],
  ['Skill watch', 'claude plugin install watch@claude-video'],
];

const falhas = [];
for (const [nome, comando, opcional] of passos) {
  console.log(`\n==> ${nome}\n    ${comando}`);
  const r = spawnSync(comando, {stdio: 'inherit', shell: true});
  if (r.status !== 0 && !opcional) falhas.push(nome);
}

// Placa Nvidia (opcional): com driver novo, instala as bibliotecas de CUDA da transcrição; com driver
// antigo, só avisa. O driver em si nunca é instalado por aqui: isso é com a pessoa (guia 1, seção 5b).
console.log('\n==> Placa de vídeo (opcional)');
let gpu = verificarGpu();
if (gpu.nvidia && gpu.driverOk && !gpu.bibliotecasCuda) {
  const cmd = `${python} -m pip install nvidia-cublas-cu12 nvidia-cudnn-cu12`;
  console.log(`    ${cmd}`);
  if (spawnSync(cmd, {stdio: 'inherit', shell: true}).status === 0) gpu = verificarGpu();
}
for (const linha of resumo(gpu)) console.log(`    ${linha}`);

for (const programa of ['ffmpeg -version', 'ffprobe -version']) {
  if (spawnSync(programa, {stdio: 'ignore', shell: true}).status !== 0) falhas.push(`${programa.split(' ')[0]} (instale pelo guia)`);
}

console.log('\n' + '='.repeat(60));
if (falhas.length === 0) {
  console.log('Tudo instalado. Abra uma sessão NOVA do Claude nesta pasta para as skills aparecerem.');
} else {
  console.log('Falhou:');
  for (const f of falhas) console.log(`  - ${f}`);
  console.log('Veja guias/1-primeiros-passos.md. Sem o comando "claude" (só Claude Desktop), a watch é');
  console.log('oferecida automaticamente ao abrir a pasta, ou instale por Personalizar > Plugins.');
}
process.exit(falhas.length === 0 ? 0 : 1);
