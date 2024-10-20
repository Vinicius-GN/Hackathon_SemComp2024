import discord
from discord.ext import commands
from discord.ui import Button, View
import api_keys
import logging

intents = discord.Intents.all()
client = commands.Bot(command_prefix="t!", intents=intents)


ticket_dict = {}

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
    # embed.add_field(name="Categorias", 
    #                 value="""Para sua conveniencia dividimos nossos 
    #                   recursos nas categorias abaixo""", 
    #                   inline=False)
    # embed.add_field(name="*Acad Arena*", 
    #                 value="""Informacoes pra voce que acabou de chegar 
    #                 e quer saber um pouco mais sobre nossa comunidade""", 
    #                 inline=False)
    # embed.add_field(name="*Documentos*", 
    #                 value="""Problemas com a validacao dos seus documentos? 
    #                 Entre nessa secao e informe-se de problemas recorrentes""",
    #                 inline=False)
    embed.add_field(name="*Ajuda*", 
                    value="""Clique no link do nosso FAQ para ser redirecionado para nossa pagina de ajuda, 
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
                    moderadores""")
    embed.set_footer(text="*Apenas contate a moderacao caso seja estritamente necessario*")

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
            ticket_dict[interaction.user] = ticket_channel

            #Ticket first message embed
            embed = discord.Embed(colour=discord.Color.purple())
            embed.add_field(name="**Atendimento Particular**",
                            value="""Aqui comeca seu atendimento com nossa moderacao,
                            envie suas duvidas ou problemas e sera respondido em 
                            breve pela nossa equipe""")
            embed.set_footer(text="Ao encerrar seu atendimento, clique no botao abaixo")
            #Ticket first message view
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
            await ticket_channel.send(embed=embed, view=view)

            #Here comes the,  part where the mods are alerted
            mod_channel = discord.utils.get(guild.channels, name="atendimentos-pendentes")
            view = View()
            view.add_item(Button(label="Atender", 
                url=f"https://discord.com/channels/{guild.id}/{ticket_channel.id}")
            )
            await mod_channel.send(f"Atendimento requisitado por {interaction.user.name}", view=view)
    
    

    view = StartView()
    # view.add_item(Button(label="Acad Arena", url="https://clonacartao.com.br/"
    #                      , style=discord.ButtonStyle.blurple))
    # view.add_item(Button(label="Documentos", url="https://clonacartao.com.br/"
    #                      , style=discord.ButtonStyle.link))
    # view.add_item(Button(label="Denuncia", url="https://clonacartao.com.br/"
    #                      , style=discord.ButtonStyle.red))
    # view.add_item(Button(label="Moderacao", url="https://clonacartao.com.br/"
    #                      , style=discord.ButtonStyle.premium))
    view.add_item(Button(label="FAQ geral", url="https://clonacartao.com.br/"
                         , style=discord.ButtonStyle.link))
    await ctx.send(view=StartView(), embed=embed)



client.run(api_keys.token_key,
log_handler=logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w'),
log_level=logging.DEBUG)

