import discord
from discord.ext import commands
from discord.ui import Button, View
import api_keys
import logging

intents = discord.Intents.all()
client = commands.Bot(command_prefix="t!", intents=intents)

# Defina o ID do canal fixo (esse é o ID do canal de suporte que você forneceu)
FIXED_CHANNEL_ID = 1297304929328828490  # Substitua pelo ID do canal onde a mensagem deve ser postada

@client.event
async def on_ready():
    """Função chamada quando o bot se conecta ao servidor e está pronto."""
    print(f'Bot conectado como {client.user}')

    # Obtém o canal de suporte pelo ID
    fixed_channel = client.get_channel(FIXED_CHANNEL_ID)
    
    # Garante que o bot não poste a mensagem duplicada se já houver mensagens fixas
    if fixed_channel:
        # Cria a visualização (view) com os botões
        class FixedButtonView(View):
            @discord.ui.button(label="Iniciar Central de Suporte", style=discord.ButtonStyle.green)
            async def startup(self, interaction: discord.Interaction, button: Button):
                # Invoca o comando startupMessage quando o botão for clicado
                await interaction.response.send_message("Iniciando Central de Suporte...")
                await send_startup_message(fixed_channel)

        # Envia a mensagem fixa no canal com o botão
        await fixed_channel.send("Clique no botão abaixo para iniciar a Central de Suporte", view=FixedButtonView())

async def send_startup_message(channel):
    """Função que envia a mensagem de suporte no canal"""
    embed = discord.Embed(
        title="💡 **Central de Suporte da Comunidade**",
        description="Aqui você pode encontrar soluções para suas dúvidas e problemas relacionados à comunidade, "
                    "bem como acessar formulários e obter suporte da nossa equipe de moderação. "
                    "Use os botões abaixo para navegar pelas opções de suporte.",
        colour=discord.Colour.blue()
    )

    embed.add_field(name="📖 **Precisa de ajuda?**",
                    value="Acesse nossa [página de suporte](https://clonacartao.com.br/) para encontrar respostas rápidas "
                          "para as dúvidas mais comuns sobre a comunidade, eventos e regras. Essa página contém tutoriais e "
                          "informações detalhadas sobre os procedimentos que seguimos.\n\n",
                    inline=False)

    embed.add_field(name="🚨 **Denunciar comportamento abusivo**",
                    value="Caso você presencie ou seja vítima de comportamentos inadequados, como assédio, bullying ou qualquer "
                          "outro tipo de abuso, clique no botão abaixo para denunciar. Nossa equipe de moderação leva todas as "
                          "denúncias a sério e tomará as medidas cabíveis para garantir a segurança e o bem-estar da comunidade.\n\n",
                    inline=False)

    embed.add_field(name="🛠️ **Relatar problemas técnicos**",
                    value="Se você encontrou algum problema técnico, como bugs no sistema ou dificuldades técnicas durante eventos, "
                          "por favor, reporte o problema clicando no botão abaixo. Nossa equipe técnica está pronta para ajudar e "
                          "trabalhar em correções o mais rápido possível.\n\n",
                    inline=False)

    embed.add_field(name="🔧 **Contato com a moderação**",
                    value="Se as opções acima não atenderem às suas necessidades, ou se você precisar de ajuda direta da equipe de moderação, "
                          "clique no botão para entrar em contato. Um canal de atendimento exclusivo será criado, onde você poderá detalhar "
                          "seu problema ou solicitar ajuda personalizada. Nossa equipe estará à disposição para te ajudar.\n\n",
                    inline=False)

    embed.add_field(name="📄 **Formulários de Solicitação**",
                    value="Precisa solicitar algo específico? Utilize nosso formulário de solicitações para os seguintes casos:\n"
                          "- **Solicitação de adiamento de partida**: Se sua equipe não puder participar de uma partida no horário agendado.\n"
                          "- **Revisão de resultados**: Caso haja necessidade de reavaliar o resultado de um jogo por algum motivo relevante.\n"
                          "- **Troca de membros da equipe**: Se for necessário alterar a composição da sua equipe, adicione ou remova jogadores.\n"
                          "- **Inscrição de novos membros**: Utilize para inscrever novos membros na equipe antes do início de um torneio.\n"
                          "Clique no botão abaixo para acessar o formulário e garantir que sua solicitação seja registrada corretamente.\n\n",
                    inline=False)

    embed.add_field(name="📚 **Suporte (FAQ)**",
                    value="Caso sua dúvida seja recorrente e relacionada a regras, regulamentos, inscrições ou procedimentos gerais, "
                          "você pode encontrar respostas rapidamente acessando nossa página de Suporte (FAQ). Esta página foi criada para "
                          "ajudar a esclarecer as dúvidas mais comuns sem a necessidade de abrir um ticket de suporte.\n\n",
                    inline=False)

    embed.set_footer(text="Estamos aqui para ajudar! Use o botão de contato com moderação.")
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1628812300470611968/ZcCTd7Yg_400x400.jpg")

    # View da mensagem inicial (botões)
    class StartView(View):
        @discord.ui.button(label="🔧 Contatar Moderação", style=discord.ButtonStyle.red)
        async def contactModerators(self, interaction: discord.Interaction, button: Button):
            await handle_moderation_request(interaction)

        @discord.ui.button(label="🚨 Denunciar Comportamento Abusivo", style=discord.ButtonStyle.blurple)
        async def reportAbusiveBehavior(self, interaction: discord.Interaction, button: Button):
            await interaction.response.send_message("Para denunciar comportamento abusivo, preencha o formulário: [Formulário de Denúncia](https://exemplo.com/denuncia)", ephemeral=True)

        @discord.ui.button(label="🛠️ Reportar Bug", style=discord.ButtonStyle.grey)
        async def reportTechIssue(self, interaction: discord.Interaction, button: Button):
            await interaction.response.send_message("Para relatar um bug, por favor, acesse o formulário: [Relatar Bug](https://exemplo.com/bug)", ephemeral=True)

        @discord.ui.button(label="📂 Formulários de Solicitação", style=discord.ButtonStyle.blurple)
        async def requestForms(self, interaction: discord.Interaction, button: Button):
            await interaction.response.send_message("Acesse os formulários de solicitação: [Formulários de Solicitação](https://exemplo.com/formularios)", ephemeral=True)

        @discord.ui.button(label="📚 Suporte (FAQ)", style=discord.ButtonStyle.green)
        async def supportFAQ(self, interaction: discord.Interaction, button: Button):
            await interaction.response.send_message("Visite a nossa página de suporte (FAQ): [FAQ](https://exemplo.com/faq)", ephemeral=True)

    # Enviar mensagem no canal
    view = StartView()
    await channel.send(embed=embed, view=view)

async def handle_moderation_request(interaction):
    """Função que lida com pedidos de contato com moderação."""
    guild = interaction.guild
    moderator_role = discord.utils.get(guild.roles, name="Moderador")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(read_messages=True),
        moderator_role: discord.PermissionOverwrite(read_messages=True)
    }
    ticket_category = await guild.create_category(
        name=f"Atendimento de {interaction.user.name}",
        overwrites=overwrites,
    )
    ticket_channel = await guild.create_text_channel(
        "Atendimento", 
        category=ticket_category,
        overwrites=overwrites
    )
    await interaction.response.send_message("Feito! Vá para o canal de atendimento.", ephemeral=True)

    message = f"Olá {interaction.user.name}, bem-vindo ao canal de atendimento. Responda algumas perguntas para "
    message += "que possamos te ajudar melhor.\n"
    message += "Em qual categoria seu problema se enquadra?"
    chosen_issue = ""
    
    def issueButtonFactory(issue: str):
        b = Button(label=issue)
        async def callback(interaction: discord.Interaction):
            nonlocal chosen_issue, issue
            chosen_issue = issue
            await interaction.response.send_message("Certo, problema identificado.", ephemeral=True)
        b.callback = callback
        return b

    class FirstTicketView(View):
        def __init__(self):
            super().__init__()
            categories = [
                "Conheça a plataforma",
                "Dúvidas sobre Aliança",
                "Sobre Competições e Ligas",
                "Problemas Técnicos",
                "Sistema de Premiação",
                "Criação e Gestão de Torneios",
                "Regras e Regulamentos",
                "Adiamento de Partidas",
                "Substituição de Membros",
                "Outro"
            ]
            for category in categories:
                self.add_item(Button(label=category, style=discord.ButtonStyle.blurple))


    await ticket_channel.send(message, view=FirstTicketView())
    
    await client.wait_for("interaction")

    message = "Por favor, descreva em detalhes o problema que está enfrentando."
    embed = discord.Embed()
    embed.set_footer(text="*Esse processo ajuda a conectar você com um moderador especializado.*")
    await ticket_channel.send(message, embed=embed)
    
    def checkMessage(m):
        return m.channel == ticket_channel and m.author != client.user
    response = await client.wait_for('message', check=checkMessage)

    faq_message = "Antes de continuar, você já verificou nossa [página de suporte](https://clonacartao.com.br/)? "
    faq_view = View()
    faq_view.add_item(Button(label="Ver FAQ", url="https://clonacartao.com.br/", style=discord.ButtonStyle.link))
    await ticket_channel.send(faq_message, view=faq_view)

    mod_channel = discord.utils.get(guild.channels, name="atendimentos-pendentes")
    view = View()
    view.add_item(Button(label="Atender", 
        url=f"https://discord.com/channels/{guild.id}/{ticket_channel.id}")
    )
    embed = discord.Embed(title=f"Atendimento requisitado por {interaction.user.name}",
                          colour=discord.Colour.blue())
    embed.add_field(name="Topico", value=chosen_issue)
    embed.add_field(name="Descrição", value=response.content)
    await mod_channel.send(embed=embed, view=view)
    
    class TerminationView(View):
        @discord.ui.button(label="Encerrar atendimento", style=discord.ButtonStyle.red)
        async def terminateTicket(self, interaction: discord.Interaction, button: Button):
            nonlocal ticket_category, ticket_channel
            await ticket_channel.delete()
            await ticket_category.delete()

            embed_back_to_start = discord.Embed(
                title="💡 **Central de Suporte da Comunidade**",
                description="Seu atendimento foi encerrado. Abaixo estão mais opções de suporte.",
                colour=discord.Colour.blue()
            )
            embed_back_to_start.add_field(name="📖 **Precisa de ajuda?**",
                                          value="Acesse nossa [página de suporte](https://clonacartao.com.br/)",
                                          inline=False)
            embed_back_to_start.add_field(name="📝 **Avaliar Atendimento**",
                                          value="Clique no botão abaixo para avaliar o atendimento prestado.",
                                          inline=False)

            evaluation_view = View()
            evaluation_view.add_item(Button(
                label="Avaliar Atendimento", 
                url="https://seuformulario.com/avaliacao",
                style=discord.ButtonStyle.link
            ))

            await interaction.user.send(embed=embed_back_to_start, view=evaluation_view)

    termination_view = TerminationView()
    message = "A moderação foi informada do seu problema. Em breve, um moderador irá te atender! Após o atendimento, por favor, avalie o serviço."
    await ticket_channel.send(message, view=termination_view)

client.run(api_keys.token_key, 
           log_handler=logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w'), 
           log_level=logging.DEBUG)
