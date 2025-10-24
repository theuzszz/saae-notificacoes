# SAAE Notificações — Portal de Interrupções e Alertas 💧⚡

Sistema simples e objetivo para divulgar **interrupções de abastecimento por bairro**, cadastrar **assinantes** e enviar **notificações** (alerta de início e normalização). Inclui **relatórios** com filtros e **exportação CSV**.

---

## ✨ Funcionalidades
- **F1**: CRUD de **Bairros** (admin)
- **F2**: CRUD de **Assinantes** (admin)
- **F3**: CRUD de **Eventos** de interrupção com **status**
- **F4**: Página pública para consulta por **bairro**
- **F5**: **Cadastro público** de assinantes
- **F6**: **Envio automático** de notificações (commands)
- **F7**: **Logs de envio** registrados
- **F8**: **Relatórios** por período com **filtros** e **CSV**
- **F9**: **Controle de acesso** via Django Admin

---

## 🏗️ Arquitetura (alto nível)
- **Django (MVC)**  
  - **Models**: `Bairro`, `Assinante`, `Evento`, `LogEnvio`  
  - **Views**: páginas públicas, API simples e relatórios  
  - **Templates**: `base.html`, `home`, `eventos`, `assinar`, `assinar_ok`, `relatorios`  
- **Commands (tarefa agendada)**  
  - `enviar_alertas`: alerta antes do início previsto  
  - `enviar_normalizacoes`: quando o evento normaliza  
- **Banco**: SQLite por padrão (opcional MySQL)  
- **E-mail**: Console (dev) ou SMTP real (produção)

---

## 🧰 Stack
- **Back-end**: Django 5  
- **Templates**: HTML + Bootstrap (responsivo)  
- **Banco**: SQLite (dev) / MySQL (opcional)  
- **Agendamento**: Windows Task Scheduler (exemplo)

---

## 🚀 Como rodar (dev)

```powershell
# Clonar
git clone https://github.com/<seu-usuario>/saae-notificacoes.git
cd saae-notificacoes

# Virtualenv
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# Dependências
pip install -r requirements.txt

# Migrações e superusuário
python manage.py migrate
python manage.py createsuperuser

# Rodar
python manage.py runserver
```

**Acesse:**
- **Público**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin  
  **Usuário:** `admin` — **Senha:** `123456789` *(ambiente de desenvolvimento)*
- **Relatórios**: http://127.0.0.1:8000/relatorios/

---

## 🗃️ Modelos (resumo)
- **Bairro**: `nome`, `ativo`  
- **Assinante**: `nome`, `email`, `telefone`, `bairro`  
- **Evento**: `bairro`, `titulo`, `descricao`, `inicio_previsto`, `fim_previsto`, `status (planejado|em_andamento|normalizado|cancelado)`  
- **LogEnvio**: `evento`, `tipo (alerta|normalizacao)`, `canal (email|sms|whatsapp)`, `destinatario`, `sucesso`, `data_envio`  

> Evita **duplicidade** de logs pelo par `(evento, destinatario, tipo)` na lógica dos commands.

---

## 🌐 Rotas úteis
- `/` — **Home** (lista bairros ativos)  
- `/bairros/<id>/` — Eventos do bairro  
- `/assinar/` — Cadastro público de assinante  
- `/api/bairros/<bairro_id>/eventos/` — JSON de eventos (simples)  
- `/relatorios/` — **Relatórios** com filtros e CSV  
- `/admin/` — Administração

**Filtros dos relatórios**  
```
?de=YYYY-MM-DD&ate=YYYY-MM-DD&status=planejado|em_andamento|normalizado|cancelado&canal=email|sms|whatsapp&tipo=alerta|normalizacao
```
Adicionar `?export=csv` para baixar o resultado como CSV.

---

## ✉️ Notificações (commands)

```powershell
# Envia alertas (próximo ao início previsto)
python manage.py enviar_alertas

# Envia normalizações (quando evento foi normalizado)
python manage.py enviar_normalizacoes
```

**Agendamento (Windows)**  
```powershell
schtasks /Create /SC MINUTE /MO 5 /TN "SAAE_enviar_alertas" ^
  /TR "\"%CD%\\.venv\\Scripts\\python.exe\" \"%CD%\\manage.py\" enviar_alertas" /F

schtasks /Create /SC MINUTE /MO 5 /TN "SAAE_enviar_normalizacoes" ^
  /TR "\"%CD%\\.venv\\Scripts\\python.exe\" \"%CD%\\manage.py\" enviar_normalizacoes" /F
```

---

## 🛠️ Configuração de e-mail

**Desenvolvimento (console)**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'nao-responder@saae.local'
```

**Produção (SMTP real)**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.seuprovedor.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'seu_usuario'
EMAIL_HOST_PASSWORD = 'sua_senha'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'alertas@saae.juazeiro.ba.gov.br'
```

---

## 🧪 Fluxo de teste (rápido)
1. Em **/admin** crie: **Bairros**, **Assinantes** (e-mail **ou** telefone), **Eventos** (início ~2h à frente, `status=planejado`).  
2. Rode `python manage.py enviar_alertas` → verifique **LogEnvio** no admin e em **/relatorios/**.  
3. Mude evento para `normalizado` → rode `python manage.py enviar_normalizacoes`.  
4. Em **/relatorios/**, aplique filtros e **Exportar CSV**.
