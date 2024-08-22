- **`+`**: Público (public)
- **`-`**: Privado (private)
- **`#`**: Protegido (protected)

### **Diagrama de Classes UML com Notação de Visibilidade**

1. **Classe `Jogo`**
   - **Atributos:**
     - `- pista: Pista`
     - `- carro_jogador: CarroJogador`
     - `- pilotos_ia: List[PilotoIA]`
     - `- ranking: Ranking`
     - `- som: Som`
     - `- interface: Interface`
     - `- dificuldade: str`
     - `- nome_jogador: str`
     - `- estado_jogo: str`
   - **Métodos:**
     - `+ iniciar_jogo()`
     - `+ iniciar_corrida()`
     - `+ pausar_jogo()`
     - `+ retomar_jogo()`
     - `+ encerrar_jogo()`
     - `+ atualizar_estado()`

2. **Classe `Pista`**
   - **Atributos:**
     - `- comprimento: int`
     - `- curvas: List[Tuple[int, int]]`
     - `- largura: int`
     - `- elementos_visuais: List[str]`
   - **Métodos:**
     - `+ desenhar()`
     - `+ verificar_saida_pista(car: Carro)`
     - `+ verificar_chegada(car: Carro)`

3. **Classe `Carro`** *(Classe Base)*
   - **Atributos:**
     - `- velocidade: float`
     - `- posicao: Tuple[int, int]`
     - `- aceleracao: float`
     - `- freio: float`
     - `- direcao: float`
     - `- sensibilidade: float`
   - **Métodos:**
     - `+ acelerar()`
     - `+ frear()`
     - `+ mover()`
     - `+ detectar_colisao()`

4. **Classe `CarroJogador`** *(Herda de `Carro`)*
   - **Métodos:**
     - `+ mover()`
     - `+ acelerar()`

5. **Classe `PilotoIA`** *(Herda de `Carro`)*
   - **Atributos:**
     - `- nivel_dificuldade: str`
   - **Métodos:**
     - `+ movimentar()`
     - `+ ajustar_velocidade()`
     - `+ decidir_movimento()`

6. **Classe `Estrategia`**
   - **Atributos:**
     - `- tipo_estrategia: str`
   - **Métodos:**
     - `+ calcular_estrategia()`

7. **Classe `PilotoAvancado`** *(Herda de `PilotoIA` e `Estrategia`)*
   - **Métodos:**
     - `+ movimentar()`
     - `+ ajustar_velocidade()`
     - `+ decidir_movimento()`

8. **Classe `Som`**
   - **Atributos:**
     - `- trilha_sonora: str`
     - `- som_colisao: str`
     - `- som_ultrapassagem: str`
     - `- som_asa_movel: str`
     - `- som_publico: str`
   - **Métodos:**
     - `+ tocar_som(evento: str)`
     - `+ tocar_trilha()`

9. **Classe `Ranking`**
   - **Atributos:**
     - `- tempos: List[Tuple[str, float]]`
   - **Métodos:**
     - `+ salvar_tempo(nome: str, tempo: float)`
     - `+ carregar_ranking()`
     - `+ exibir_ranking()`

10. **Classe `Interface`**
   - **Atributos:**
     - `- cronometro: str`
     - `- posicao_corrida: int`
     - `- mensagem: str`
   - **Métodos:**
     - `+ desenhar_cronometro()`
     - `+ desenhar_posicao()`
     - `+ exibir_mensagem(mensagem: str)`

### **Relações**

- **Herança:**
  - `CarroJogador` <- `Carro` (herança pública)
  - `PilotoIA` <- `Carro` (herança pública)
  - `PilotoAvancado` <- `PilotoIA` + `Estrategia` (herança múltipla)

- **Composição:**
  - `Jogo` -> `Pista`
  - `Jogo` -> `CarroJogador`
  - `Jogo` -> `PilotoIA`
  - `Jogo` -> `Som`
  - `Jogo` -> `Ranking`
  - `Jogo` -> `Interface`

Lucidchart, draw.io (diagrams.net), StarUML, ou Visual Paradigm para desenhar o diagrama com a notação UML. 