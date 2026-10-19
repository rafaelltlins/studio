import React from 'react';
import {Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

// Figurinha 3D da biblioteca comum (projetos/_biblioteca/figurinhas/, catálogo no LEIA-ME de lá).
// Use dentro de uma <Sequence> que começa na palavra-gatilho: entra girando com mola elástica,
// balança e flutua de leve e sai encolhendo nos últimos `saida` quadros. `quica` faz pular no lugar (bom para CTA).

const PASTA = '_biblioteca/figurinhas';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

export const Figurinha: React.FC<{
  nome: string; left: number; top: number; tamanho: number;
  atraso?: number; giro?: number; quica?: boolean; saida?: number;
}> = ({nome, left, top, tamanho, atraso = 0, giro = 0, quica = false, saida = 9}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const t = frame - atraso;
  const entra = spring({frame: t, fps, config: {damping: 8, stiffness: 160, mass: 0.7}});
  const sai = interpolate(frame, [durationInFrames - saida, durationInFrames], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const balanco = Math.sin(t / 7) * 4;
  const flutua = quica ? -Math.abs(Math.sin(t / 6)) * 34 : Math.sin(t / 11) * 7;
  return (
    <Img
      src={staticFile(`${PASTA}/${nome}`)}
      style={{
        position: 'absolute', left, top, width: tamanho, height: tamanho,
        filter: 'drop-shadow(0 16px 22px rgba(0,0,0,.35))',
        opacity: t < 0 ? 0 : Math.min(entra * 2, 1) * (1 - sai),
        scale: String(entra * (1 - sai * 0.4)),
        rotate: `${interpolate(entra, [0, 1], [giro - 30, giro]) + balanco}deg`,
        translate: `0px ${flutua}px`,
      }}
    />
  );
};
