# Como contribuir

Contribuições são bem-vindas, principalmente as que vêm de uso real.

## O que ajuda mais
1. **Relato de uso.** Você usou a skill num business case de verdade? Abra uma issue dizendo o que funcionou, o que travou e o que o agente errou. Não inclua dados confidenciais.
2. **Perfil de nicho novo.** Copie `business-case/references/perfis/_modelo.md`, preencha e abra um pull request.
3. **Correção do roteiro ou do script.**

## Regras
- **Toda mudança parte de uma falha observada.** Descreva o caso em que a skill errou ou ficou aquém. Mudança só de estilo não entra.
- **Perfil não traz número pronto.** Referência de mercado só com fonte e data. Sem isso, escreva a pergunta que leva ao dado.
- **Nada de dados reais** de empresas ou pessoas nos exemplos. Use dados fictícios e diga que são fictícios.
- **O roteiro fica curto.** O que for detalhe vai para `references/`. Se a mudança aumentar o `SKILL.md`, diga o que pode sair.
- **Mudou o script?** Rode os testes e acrescente um teste para o caso novo:

```bash
python3 -m unittest discover -s tests -v
```

## Idioma
Português do Brasil, em linguagem simples.
