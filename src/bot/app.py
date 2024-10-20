import discord
from discord.ext import commands
from discord.ui import Button, View
import api_keys
import logging

intents = discord.Intents.all()
client = commands.Bot(command_prefix="t!", intents=intents)



@client.command()
async def startupMessage(ctx : commands.Context):
    """Should be called once to init the help message"""

    
    #The embed of the startup message
    embed = discord.Embed(
        title="**Central de ajuda**",
        colour=discord.Colour.purple())
    embed.add_field(name="Novo por aqui? Com duvidas?",
                    value="""Siga os links abaixo para obter respostas para duvidas frequentes,  
                    ou conversar com os moderadores se for neccessario""",
                    inline=False)
    embed.add_field(name="*Suporte*", 
                    value="""Clique no link da nossa Pagina de Suporte para ser redirecionado, 
                    onde voce encontra informacoes sobre nossa comunidade, duvidas frequentes e informcacoes 
                    sobre torneios""", 
                    inline=False)
    embed.add_field(name="*Denunciar abuso*", 
                    value="""Nao ha espaco para intolerancia e violencia 
                    na nossa comunidade, caso presencie alguma situacao do tipo, 
                    nao hesite em denunciar a nossa equipe pelo link abaixo""", 
                    inline=False)
    embed.add_field(name="*Contatar moderacao*", 
                    value="""Caso seu problema nao possa ser solucionado 
                    pelas opcoes anteriores, voce pode contatar nossa equipe de 
                    moderadores
                    Caso deseje contatar a moderacao, clique no botao e sera criada uma sala \"atendimento\" 
                    com seu nome, na qual seu atendimento prosseguira, voce deve entrar manualmente nela""")
    embed.add_field(name="*Reportar Bug*", 
                    value="""Nada eh perfeito e podem haver erros, caso encontre algum, avise pra gente!""", 
                    inline=False)
    embed.set_footer(text="*Apenas contate a moderacao caso seja estritamente necessario*")
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1628812300470611968/ZcCTd7Yg_400x400.jpg")

    #View of the startup message
    class StartView(View):
        #Button to contact moderators
        @discord.ui.button(label="Moderacao", 
                           style=discord.ButtonStyle.red)
        async def contactModerators(self, interaction : discord.Interaction,
                                    button : Button):
            guild = interaction.guild
            moderator_role = discord.utils.get(
                guild.roles, 
                name="Moderador"
            )
            #Only the ticket emitter and the modderation have access to the channel
            overwrites = {
                guild.default_role : discord.PermissionOverwrite(read_messages=False),
                interaction.user : discord.PermissionOverwrite(read_messages=True),
                moderator_role : discord.PermissionOverwrite(read_messages=True)
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
            await interaction.response.send_message("Feito! Siga para o canal de atendimento", ephemeral=True)

            #Ticket first message embed
           

            message = f"Ola {interaction.user.name}, bem vindo ao canal de atendimento, antes de prosseguirmos "
            message += "responda algumas perguntas para que possamos te ajudar melhor.\n"
            message += "Em qual categoria seu problema melhor se enquadra?"
            chosen_issue = ""
            def issueButtonFactory(issue:str):
                b = Button(label=issue)
                async def callback(interaction : discord.Interaction):
                    nonlocal chosen_issue, issue
                    chosen_issue = issue
                    await interaction.response.send_message("Certo", ephemeral=True)
                b.callback = callback
                return b
            class FirstTicketView(View):
                def __init__(self):
                    super().__init__()
                    for i in ["Documentos", "Torneios", "Outro"]:
                        self.add_item(issueButtonFactory(i))
            await ticket_channel.send(message, view=FirstTicketView())
            
            def checkInteraction(i):
                nonlocal interaction
                return interaction.channel == ticket_channel
            await client.wait_for("interaction")

            message = "Otimo! Agora voce pode dar uma descricao em texto de que tipo de problema esta enfrentando"
            message +="\nObs: So precisa enviar como mensagem nesse chat"
            embed = discord.Embed()
            embed.set_footer(text="*Este processo garante que um moderador que entende do seu problema ira atende-lo*")
            await ticket_channel.send(message, embed=embed)
            
            def checkMessage(m):
                return m.channel == ticket_channel and m.author != client.user
            response = await client.wait_for('message', check=checkMessage)
            

            #Here comes the,  part where the mods are alerted
            mod_channel = discord.utils.get(guild.channels, name="atendimentos-pendentes")
            view = View()
            view.add_item(Button(label="Atender", 
                url=f"https://discord.com/channels/{guild.id}/{ticket_channel.id}")
            )
            embed = discord.Embed(title=f"Atendimento requisitado por {interaction.user.name}",
                                  colour=discord.Colour.purple()
                                  )
            embed.add_field(name="Topico", value=chosen_issue)
            embed.add_field(name="Descricao", value=response.content)
            await mod_channel.send(embed=embed, view=view)
            
            #Ticket termination message view

            class TerminationView(View):
                #Ticket termination button
                @discord.ui.button(label="Encerrar atendimento", 
                                   style=discord.ButtonStyle.red)
                async def terminateTicket(self, interaction : discord.Interaction,
                                    button : Button):
                    nonlocal ticket_category, ticket_channel
                    await ticket_channel.delete()
                    await ticket_category.delete()
            view = TerminationView()
            message = "Tudo pronto! A moderacao foi informada do seu problema"
            message += "\nEm breve um moderador te atendera por esse canal. Fique antenado!"
            await ticket_channel.send(message, view=view)

            
    
    

    view = StartView()
    view.add_item(Button(label="Denuncia", url="https://clonacartao.com.br/"
                         , style=discord.ButtonStyle.red))
    view.add_item(Button(label="Suporte", url="https://clonacartao.com.br/"
                         , style=discord.ButtonStyle.link))
    view.add_item(Button(label="Reportar Bug", url="https://clonacartao.com.br/"
                         , style=discord.ButtonStyle.link))
    await ctx.send(view=view, embed=embed)



client.run(api_keys.token_key,
log_handler=logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w'),
log_level=logging.DEBUG)

