import React from 'react';
import {Composition, Folder} from 'remotion';
import {MinimalSuico} from './estilos/MinimalSuico';
import {TerminalTecnico} from './estilos/TerminalTecnico';
import {VerticalDados} from './estilos/VerticalDados';
import {VerticalLegendas} from './estilos/VerticalLegendas';
import {VerticalPrint} from './estilos/VerticalPrint';

const FPS = 30;
const SEIS_SEGUNDOS = 6 * FPS;

// Seus vídeos ficam em src/videos/<slug>/ e cada um tem um registro.tsx (export default com o seu
// <Folder> e as <Composition>). Eles são encontrados aqui automaticamente e não vão para o Git
// (src/videos/* está no .gitignore), então este arquivo não precisa ser editado a cada vídeo.
type ModuloDeRegistro = {default: React.FC};
type ContextoDoWebpack = {keys(): string[]; (caminho: string): ModuloDeRegistro};
const contexto = (require as unknown as {context(pasta: string, subpastas: boolean, filtro: RegExp): ContextoDoWebpack}).context(
  './videos',
  true,
  /^\.\/[^/]+\/registro\.tsx$/,
);
const registros = contexto
  .keys()
  .sort()
  .map((caminho) => ({caminho, Registro: contexto(caminho).default}));

export const RemotionRoot: React.FC = () => (
  <>
    {/* Exemplos que rodam sem nenhum vídeo. Servem de referência de estilo, não de padrão fixo. */}
    <Folder name="Estilos">
      <Composition id="MinimalSuico" component={MinimalSuico} width={1920} height={1080} fps={FPS} durationInFrames={SEIS_SEGUNDOS} />
      <Composition id="TerminalTecnico" component={TerminalTecnico} width={1920} height={1080} fps={FPS} durationInFrames={SEIS_SEGUNDOS} />
      <Composition id="VerticalLegendas" component={VerticalLegendas} width={1080} height={1920} fps={FPS} durationInFrames={SEIS_SEGUNDOS} />
      <Composition id="VerticalPrint" component={VerticalPrint} width={1080} height={1920} fps={FPS} durationInFrames={SEIS_SEGUNDOS} />
      <Composition id="VerticalDados" component={VerticalDados} width={1080} height={1920} fps={FPS} durationInFrames={SEIS_SEGUNDOS} />
    </Folder>

    {registros.map(({caminho, Registro}) => (
      <Registro key={caminho} />
    ))}
  </>
);
