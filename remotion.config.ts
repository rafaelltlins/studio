import {Config} from '@remotion/cli/config';

Config.setCodec('h264');
Config.setVideoImageFormat('jpeg');
Config.setPixelFormat('yuv420p');
Config.setOverwriteOutput(true);
// Tudo que está em projetos/ pode ser usado com staticFile('<NNN. slug>/...').
Config.setPublicDir('projetos');
// O cache persistente do webpack falha com EPERM em algumas instalações do Windows.
Config.setCachingEnabled(false);
// Desenha os quadros com a placa de vídeo (ANGLE/Direct3D no Windows) em vez de só na CPU:
// ~15% mais rápido numa GTX 1660 Ti, com resultado visual igual. Sem GPU, o Chrome cai no modo por software.
Config.setChromiumOpenGlRenderer('angle');
