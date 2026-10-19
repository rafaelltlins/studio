# src/videos

Código de cada vídeo editado no Remotion: uma pasta por vídeo, `src/videos/<slug>/`.

- Tudo aqui dentro fica **fora do Git** (`src/videos/*` no `.gitignore`), exceto este arquivo. Os seus vídeos são trabalho seu e dependem de arquivos de `projetos/`, que também não são versionados.
- Cada pasta precisa de um `registro.tsx` com `export default` de um componente que devolve o `<Folder name="NNN-slug">` com as `<Composition>` do vídeo. O `src/Root.tsx` encontra esses arquivos sozinho; não é preciso editá-lo.

Exemplo mínimo de `src/videos/meu-video/registro.tsx`:

```tsx
import React from 'react';
import {Composition, Folder} from 'remotion';
import {MeuVideo} from './MeuVideo';

const Registro: React.FC = () => (
  <Folder name="001-meu-video">
    <Composition id="MeuVideo" component={MeuVideo} width={1080} height={1920} fps={30} durationInFrames={900} />
  </Folder>
);

export default Registro;
```
