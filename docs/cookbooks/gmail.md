# Extração de dados do gmail

Alguns projetos como o [armazem-siafi-dados](https://github.com/splor-mg/armazem-siafi-dados) precisam de realizar download de arquivos do gmail durante a execução da etapa de extração. 
Atualmente utilizamos o pacote [gmailr](https://github.com/r-lib/gmailr/) do R para implementar os scripts de extração nestes projetos.

Como o download de arquivos do gmail exige autenticação, para execução da etapa de extração via Github Actions é necessário uma etapa adicional de configuração.

A configuração consiste em salvar um token criptografado no repositório do projeto (eg. `gmailr.rds`) e uma chave privada no Github Actions [secret](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) (eg. `GMAILR_KEY`).

Com esse par de informação o script de extração consegue fazer autenticação e download dos arquivos.

## Criação de um client OAuth

Via de regra não será necessário criar um client OAuth[^20240130T100107].
Em caso de dúvida, 
converse com seu coleguinha.

Caso realmente seja necessário siga as instruções disponíveis em [Set up an OAuth client • gmailr](https://gmailr.r-lib.org/dev/articles/oauth-client.html).

[^20240130T100107]: Uma boa leitura para entender mais sobre OAuth de forma geral é [OAuth • httr2](https://httr2.r-lib.org/articles/oauth.html).

## Criação do token gmail.rds

!!! note

    Se você está criando um novo repositório anual (eg. `armazem-siafi-dados-2024`) a partir de um repositório upstream (eg. `armazem-siafi-dados`) é provável que o token `gmail.rds` já esteja criado e armazenado no repositório. 

    Nesse caso, siga as [instruções](#disponibilizacao-da-chave-privada-gmailr_key-para-o-github-actions) para disponibilizar a informação da chave privada para o Github Actions.

Na pasta do projeto execute[^20240130T102409] no console do R:

[^20240130T102409]: Instruções adaptadas de [Deploy a token](https://cran.r-project.org/web/packages/gmailr/vignettes/deploy-a-token.html)

```r
library(gmailr)

gm_auth_configure(path = '~/.gmailr/credentials.json') # path/to/your/oauth_client.json
gm_auth(email='dcmefo.scppo@gmail.com', cache = FALSE)

gmailr_key <- gargle::secret_make_key() # string aleatória utilizada como chave de criptografia
Sys.setenv(GMAILR_KEY = gmailr_key)
Sys.getenv("GMAILR_KEY") # anote este valor

gm_token_write(path = 'gmail.rds', key = "GMAILR_KEY")
```

Como nosso token fica exposto no Github ele deve ser criptografado. 
A função [`gargle::secret_make_key()`](https://gargle.r-lib.org/reference/gargle_secret.html) é usada para gerar uma string aleatória que pode ser usada como chave de criptografia. 
A mesma chave precisa estar disponível como uma variável de ambiente `GMAILR_KEY` no seu ambiente de desenvolvimento local para geração do token e no Github Actions para que o token armazenado no arquivo `gmail.rds` possa ser descriptografado.

!!! warning

    Na mensagem:

    ```
    Is it OK to cache OAuth access credentials in the folder ~/Library/Caches/gargle
    between R sessions?
    1: Yes
    2: No
    ```

    Escolher `No` caso contrário em um segundo computador a execução não vai funcionar com o erro:

    ```
    Warning message:
    In gzfile(file, mode) :
    cannot open compressed file 'C:/Users/Henrique/AppData/Local/gargle/gargle/Cache/c123167a8057ead5095cb72c1b2704a6_dcmefo.scppo@gmail.com', probable reason 'No such file or directory'
    Execution halted
    ```

## Disponibilização da chave privada GMAILR_KEY para o Github Actions

No nosso plano atual do Github para a organização `splor-mg` "organization secrets and variables cannot be used by private repositories".
Portanto é necessário criar o segredo `GMAILR_KEY` em cada repositório que precisa de realizar extração.

!!! note

    Importante lembrar que a variável de ambiente `GMAILR_KEY` deve estar disponível dentro do container (ie. [https://github.com/splor-mg/armazem-siafi-totais-dados/tree/547e22165dcc6924b9d2dab80e5eee444b768471](https://github.com/splor-mg/armazem-siafi-totais-dados/tree/547e22165dcc6924b9d2dab80e5eee444b768471))

