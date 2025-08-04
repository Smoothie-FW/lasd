# LASD Mass Shift
import discord
from discord import app_commands, Interaction, Embed, User
from discord.ext import commands, tasks
from discord.ui import View, Button
import os
from dotenv import load_dotenv
from typing import Literal
import asyncio
from datetime import datetime, timedelta
import json
import aiohttp




print("Loaded token:", os.getenv("BOT_TOKEN"))  # Make sure this prints correctly


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True


bot = commands.Bot(command_prefix="-", intents=intents)


from discord.ext import commands
from discord import app_commands, Interaction, Embed, ButtonStyle, AllowedMentions, ui
from discord.ui import View, Button


class VoteView(View):
   def __init__(self, vote_goal: int):
       super().__init__(timeout=None)
       self.voters = set()
       self.vote_goal = vote_goal


   @ui.button(label="Vote", style=ButtonStyle.success, emoji="✅")
   async def vote(self, interaction: Interaction, button: Button):
       user = interaction.user


       if user.id in self.voters:
           class LeaveView(View):
               def __init__(self, parent_view):
                   super().__init__(timeout=None)
                   self.parent_view = parent_view


               @ui.button(label="Leave Mass Shift", style=ButtonStyle.danger)
               async def leave(self, leave_interaction: Interaction, _):
                   await leave_interaction.response.defer(ephemeral=True)
                   if user.id in self.parent_view.voters:
                       self.parent_view.voters.remove(user.id)
                       await leave_interaction.followup.send("✅ Successfully removed your vote from the mass-shift.", ephemeral=True)
                   else:
                       await leave_interaction.followup.send("You're not in the vote list.", ephemeral=True)


           await interaction.response.defer(ephemeral=True)
           await interaction.followup.send(
               "❌ You have already voted.",
               view=LeaveView(self),
               ephemeral=True
           )
           return


       self.voters.add(user.id)
       await interaction.response.send_message("✅ Your vote has been counted.", ephemeral=True)


       if len(self.voters) >= self.vote_goal:
           mentions = " ".join(f"<@{uid}>" for uid in self.voters)
           await interaction.channel.send(f"✅ Vote goal reached!\n{mentions}")
           button.disabled = True
           await interaction.message.edit(view=self)


   @ui.button(label="Attendees", style=ButtonStyle.secondary)
   async def attendees(self, interaction: Interaction, _):
       if not self.voters:
           await interaction.response.send_message("No one has voted yet.", ephemeral=True)
       else:
           names = "\n".join(f"<@{uid}>" for uid in self.voters)
           await interaction.response.send_message(f"📝 **Current Attendees:**\n{names}", ephemeral=True)


@bot.tree.command(name="mass-shift", description="Start a LASD Mass Shift announcement")
@app_commands.describe(
   votes="Number of votes needed",
   promotional="Is it promotional? (yes or no)"
)
async def mass_shift(interaction: Interaction, votes: int, promotional: str):
   allowed_roles = [1311735780766646393, 1311735780783292477, 1354280877646942309, 1340506488187392080, 1316556364285218827]
   ping_role_id = 1311735780699537457
   channel_id = 1339061804684414997


   member_roles = [role.id for role in interaction.user.roles]
   if not any(role in allowed_roles for role in member_roles):
       await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
       return


   await interaction.response.send_message(
       f"✅ Successfully started a LASD Mass Shift. https://discord.com/channels/{interaction.guild.id}/{channel_id}",
       ephemeral=True
   )


   channel = bot.get_channel(channel_id)
   if channel is None:
       return


   await channel.purge(limit=100)


   embed = Embed(
       title="A Mass Shift Has Started!",
       description="A High Ranking Member is hosting a Mass Shift.\nIf you are planning on attending, please press the green button below.",
       color=0x795c33
   )
   embed.add_field(name="⎯⎯⎯⎯⎯⎯⎯", value=f"**Votes Needed:** {votes}", inline=False)
   embed.add_field(name="⎯⎯⎯⎯⎯⎯⎯", value=f"**Promotional:** {promotional.upper()}", inline=False)
   embed.add_field(name="⎯⎯⎯⎯⎯⎯⎯", value=f"**Host:** {interaction.user.mention}", inline=False)
   embed.add_field(name="⎯⎯⎯⎯⎯⎯⎯", value="Vote by pressing the green button below:", inline=False)


   view = VoteView(vote_goal=votes)


   await channel.send(
       content=f"<@&{ping_role_id}>",
       embed=embed,
       view=view,
       allowed_mentions=AllowedMentions(roles=True)
   )












#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯


# LASD Promotion


@bot.tree.command(name="promote", description="Announce a promotion.")
@app_commands.describe(promoted_member="Select the user being promoted", new_rank="Select the new role/rank", reason="What is the reason for the promotion?")
async def promote(
   interaction: discord.Interaction,
   promoted_member: discord.User,
   new_rank: discord.Role,
   reason: str
):
   allowed_roles = [1311735780766646393, 1311735780783292477, 1354280877646942309, 1340506488187392080, 1316556364285218827]
   member_roles = [role.id for role in interaction.user.roles]
   if not any(role in allowed_roles for role in member_roles):
       await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
       return


   channel = bot.get_channel(1311735781685071958)
   embed = discord.Embed(
       title=":tada: Deputy Promotion",
       description=(
           f"Dear, {promoted_member.mention} We appreciate your dedication to LASD. We are pleased to inform you about your promotion to {new_rank.mention} Your hard work and contribution is the reason you earned this position.\n"
           f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
           f"> **Promoted Member:** {promoted_member.mention}\n"
           f"> **New Rank:** {new_rank.mention}\n"
           f"> **Reason:** {reason}\n"
           f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
           f"-# **Signed By:** {interaction.user.mention}\n"
       ),
       color=discord.Color.dark_gold()
   )
   embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1311735780783292482/1311742608334262375/png-clipart-los-angeles-county-sheriff-s-department-police-claremont-board-of-supervisors-sheriff-removebg-preview.png")
   embed.set_image(url="https://cdn.discordapp.com/attachments/1395864225418575985/1401650550625534133/image.png?ex=68910c4c&is=688fbacc&hm=c8246710a2157dbc9ea271fa9b655c1813baa37c76be688174546109409e2cff&")


   await channel.send(content=promoted_member.mention, embed=embed)


   try:
       await promoted_member.send(":tada: You were promoted in the Los Angeles Sheriff's Department!")
   except discord.Forbidden:
       await interaction.response.send_message("Promotion posted, but I couldn't DM the user.", ephemeral=True)
       return


   await interaction.response.send_message("Promotion posted successfully and DM sent.", ephemeral=True)






#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯


# LASD INFRACT
@bot.tree.command(name="infract", description="Announce a infraction.")
@app_commands.describe(infracted_member="Select the user being infracted", punishment="What punishment are they receiving?", reason="What is the reason for the infraction?")
async def infract(
   interaction: discord.Interaction,
   infracted_member: discord.User,
   punishment: Literal["Notice", "Warning", "Strike", "Demotion", "Under Investigation", "Suspension", "Termination", "Blacklist"],
   reason: str
):
   allowed_roles = [1311735780766646393, 1311735780783292477, 1354280877646942309, 1340506488187392080, 1316556364285218827]
   member_roles = [role.id for role in interaction.user.roles]
   if not any(role in allowed_roles for role in member_roles):
       await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
       return


   channel = bot.get_channel(1311735781685071960)
   embed = discord.Embed(
       title=":x: Deputy Infraction",
       description=(
           f"You have been infracted by {interaction.user.mention}. If you believe this is a false infraction, you can create a ticket in https://discord.com/channels/1311735780699537452/1311735781273894934 or appeal later on.\n"
           f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
           f"> **User:** {infracted_member.mention}\n"
           f"> **Infraction:** {punishment}\n"
           f"> **Reason:** {reason}\n"
           f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
           f"-# **Signed By:** {interaction.user.mention}\n"
       ),
       color=discord.Color.dark_gold()
   )
   embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1311735780783292482/1311742608334262375/png-clipart-los-angeles-county-sheriff-s-department-police-claremont-board-of-supervisors-sheriff-removebg-preview.png")
   embed.set_image(url="https://cdn.discordapp.com/attachments/1395864225418575985/1401650653368942733/image.png?ex=68910c65&is=688fbae5&hm=9102581f66b4a71f9579c5273061492af2373ae2a45d2c1c16258cf7e3d3708c&")


   await channel.send(content=infracted_member.mention, embed=embed)


   # ✅ Add infraction to JSON file
   save_infraction(
       user_id=infracted_member.id,
       staff_id=interaction.user.id,
       punishment=punishment,
       reason=reason
   )


   try:
       await infracted_member.send(":x: You were infracted in the Los Angeles Sheriff's Department!")
   except discord.Forbidden:
       await interaction.response.send_message("Infraction posted, but I couldn't DM the user.", ephemeral=True)
       return


   await interaction.response.send_message("Infraction posted successfully and DM sent.", ephemeral=True)








# INFRACTIONS LIST
INFRACTIONS_FILE = "infractions.json"


def load_infractions():
   try:
       with open(INFRACTIONS_FILE, "r") as f:
           data = f.read().strip()
           return json.loads(data) if data else {}
   except (json.JSONDecodeError, FileNotFoundError):
       return {}


def save_infraction(user_id, staff_id, punishment, reason):
   data = load_infractions()
   entry = {
       "by": staff_id,
       "punishment": punishment,
       "reason": reason,
       "timestamp": datetime.utcnow().isoformat()
   }
   data.setdefault(str(user_id), []).append(entry)
   with open(INFRACTIONS_FILE, "w") as f:
       json.dump(data, f, indent=4)


@bot.tree.command(name="infractions-list", description="View a user's past infractions")
@app_commands.describe(user="The user to check infractions for")
@app_commands.guilds(discord.Object(id=1311735780699537452))  # TEMP: fast sync to your test guild
async def infractions_list(interaction: discord.Interaction, user: discord.User):
   allowed_roles = [
       1311735780766646393,
       1311735780783292477,
       1354280877646942309,
       1340506488187392080,
       1316556364285218827,
       1311735780745416813
   ]
   if not any(role.id in allowed_roles for role in interaction.user.roles):
       await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
       return


   data = load_infractions()
   user_infractions = data.get(str(user.id), [])


   if not user_infractions:
       await interaction.response.send_message(f"{user.mention} has no infractions logged.", ephemeral=True)
       return


   embed = discord.Embed(
       title=f"📋 Infractions for {user}",
       color=discord.Color.red()
   )


   for i, inf in enumerate(user_infractions[:25], start=1):
       embed.add_field(
           name=f"Infraction #{i}",
           value=f"> **By:** <@{inf['by']}>\n> **Type:** {inf['punishment']}\n> **Reason:** {inf['reason']}\n> **Date:** {inf.get('timestamp', 'N/A')}",
           inline=False
       )


   await interaction.response.send_message(embed=embed, ephemeral=True)




#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
# LASD Warrant


# Autocomplete function
async def roblox_username_autocomplete(interaction: discord.Interaction, current: str):
    if not current:
        return []
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://users.roblox.com/v1/users/search?keyword={current}&limit=10") as resp:
            if resp.status != 200:
                return []
            data = await resp.json()
            return [
                app_commands.Choice(name=user["name"], value=user["name"])
                for user in data.get("data", [])
            ]

# Get Roblox user ID from username
async def get_roblox_user_id(username: str):
    async with aiohttp.ClientSession() as session:
        async with session.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [username]}) as resp:

            if resp.status != 200:
                return None
            data = await resp.json()
            try:
                return data["data"][0]["id"]
            except (KeyError, IndexError):
                return None

@bot.tree.command(name="log-warrant", description="Logs a warrant")
@app_commands.describe(
    suspect="What is the Roblox username of the suspect?",
    charges="What are the charges of the suspect?"
)
@app_commands.autocomplete(suspect=roblox_username_autocomplete)
async def log_warrant(
    interaction: discord.Interaction,
    suspect: str,
    charges: str
):
    allowed_roles = [1311735780699537457, 1316556364285218827, 1340506488187392080, 1354280877646942309]
    member_roles = [role.id for role in interaction.user.roles]
    if not any(role in allowed_roles for role in member_roles):
        await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
        return

    user_id = await get_roblox_user_id(suspect)
    if not user_id:
        await interaction.response.send_message("❌ Unable to find that Roblox user.", ephemeral=True)
        return

    avatar_url = f"https://www.roblox.com/headshot-thumbnail/image?userId={user_id}&width=420&height=420&format=png"

    channel = bot.get_channel(1340799241639039007)
    embed = discord.Embed(
        title="LASD Warrant",
        description=(
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"**Deputy:** {interaction.user.mention}\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"**Suspect:** {suspect}\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"**Charges:** {charges}\n"
        ),
        color=discord.Color.dark_gold()
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1311735780783292482/1311742608334262375/png-clipart-los-angeles-county-sheriff-s-department-police-claremont-board-of-supervisors-sheriff-removebg-preview.png")
    embed.set_image(url=avatar_url)

    await channel.send(embed=embed)
    await interaction.response.send_message("✅ Warrant has been logged.", ephemeral=True)




#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
#LASD Traffic Stop
@bot.tree.command(name="log-traffic-stop", description="Logs a traffic stop.")
@app_commands.describe(
   suspect="Roblox username of the suspect",
   reason="Reason for the traffic stop",
   punishment="Punishment given to the suspect",
   evidence="Upload an image of the stop (attachment)"
)
async def log_traffic_stop(
   interaction: discord.Interaction,
   suspect: str,
   reason: str,
   punishment: str,
   evidence: discord.Attachment
):
   allowed_roles = [1311735780699537457, 1316556364285218827, 1340506488187392080, 1354280877646942309]
   member_roles = [role.id for role in interaction.user.roles]
   if not any(role in allowed_roles for role in member_roles):
       await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
       return


   channel = bot.get_channel(1311735781685071956)
   embed = discord.Embed(
       title="Traffic Stop Log",
       description=(
           f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
           f"**Deputy:** {interaction.user.mention}\n"
           f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
           f"**Suspect:** `{suspect}`\n"
           f"**Reason:** `{reason}`\n"
           f"**Punishment:** `{punishment}`\n"
           f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
       ),
       color=discord.Color.dark_gold()
   )
   embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1311735780783292482/1311742608334262375/png-clipart-los-angeles-county-sheriff-s-department-police-claremont-board-of-supervisors-sheriff-removebg-preview.png")
   embed.set_image(url=evidence.url)


   await channel.send(embed=embed)
   await interaction.response.send_message("✅ Traffic stop log submitted.", ephemeral=True)














#suspesnsion
















# Suspension config
SUSPENSION_FILE = "suspensions.json"
LOG_CHANNEL_ID = 1392197423664992266
TEMP_ROLE = 1311735780711989310
KEEP_ROLE = 1311735780745416813
ALLOWED_ROLE_IDS = [
   1311735780766646393,
   1311735780783292477,
   1340506488187392080,
   1316556364285218827,
   1354280877646942309
]


# Suspension file setup
if not os.path.exists(SUSPENSION_FILE):
   with open(SUSPENSION_FILE, "w") as f:
       json.dump({}, f)


def load_suspensions():
   try:
       with open(SUSPENSION_FILE, "r") as f:
           data = f.read().strip()
           return json.loads(data) if data else {}
   except json.JSONDecodeError:
       return {}


def save_suspensions(data):
   with open(SUSPENSION_FILE, "w") as f:
       json.dump(data, f, indent=4)


# Background check to restore roles
@tasks.loop(minutes=1)
async def check_suspensions():
   now = datetime.utcnow()
   data = load_suspensions()
   to_remove = []


   for user_id, info in data.items():
       restore_time = datetime.fromisoformat(info["restore_time"])
       if now >= restore_time:
           guild = bot.get_guild(int(info["guild_id"]))
           try:
               member = await guild.fetch_member(int(user_id))
           except discord.NotFound:
               continue




           if member:
               # Restore original roles
               for role_id in info["roles"]:
                   role = guild.get_role(role_id)
                   if role:
                       await member.add_roles(role, reason="Suspension period over")


               # Remove TEMP_ROLE
               temp_role = guild.get_role(TEMP_ROLE)
               if temp_role in member.roles:
                   await member.remove_roles(temp_role, reason="End of suspension")
           to_remove.append(user_id)


   for user_id in to_remove:
       data.pop(user_id)
   if to_remove:
       save_suspensions(data)






@bot.tree.command(name="suspend", description="Suspend a user by removing their roles temporarily.")
@app_commands.describe(user="User to suspend", reason="Reason for suspension", days="Duration in days")
async def suspend(interaction: discord.Interaction, user: discord.Member, reason: str, days: int):
   if not any(role.id in ALLOWED_ROLE_IDS for role in interaction.user.roles):
       await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
       return


   if user == interaction.user:
       await interaction.response.send_message("You cannot suspend yourself.", ephemeral=True)
       return


   await interaction.response.defer(thinking=True, ephemeral=True)


   roles_to_remove = [role.id for role in user.roles if role != user.guild.default_role]
   if not roles_to_remove:
       await interaction.followup.send("User has no roles to suspend.", ephemeral=True)
       return


   await user.remove_roles(*[discord.Object(id=r) for r in roles_to_remove], reason=reason)
   await user.add_roles(
       discord.Object(id=TEMP_ROLE),
       discord.Object(id=KEEP_ROLE),
       reason="Suspended"
   )


   data = load_suspensions()
   data[str(user.id)] = {
       "guild_id": str(interaction.guild_id),
       "roles": roles_to_remove,
       "restore_time": (datetime.utcnow() + timedelta(days=days)).isoformat()
   }
   save_suspensions(data)


   try:
       await user.send(
           f"You have been suspended from **{interaction.guild.name}** for **{days} day(s)**.\nReason: {reason}"
       )
   except discord.Forbidden:
       pass


   log_channel = bot.get_channel(LOG_CHANNEL_ID)
   if log_channel:
       embed = discord.Embed(
           title="User Suspended",
           description=f"**User:** {user.mention}\n**By:** {interaction.user.mention}\n**Reason:** {reason}\n**Duration:** {days} day(s)",
           color=discord.Color.orange()
       )
       await log_channel.send(embed=embed)


   await interaction.followup.send(
       f"🔨 Suspended {user.mention} for {days} day(s).\nReason: {reason}",
       ephemeral=True
   )








































#unsuspend
import discord
from discord.ext import commands
from discord import app_commands, Interaction, Embed
import json


SUSPENSION_FILE = "suspensions.json"
LOG_CHANNEL_ID = 1392197423664992266
TEMP_ROLE = 1311735780711989310
ALLOWED_ROLE_IDS = [
   1311735780766646393,
   1311735780783292477,
   1340506488187392080,
   1316556364285218827,
   1354280877646942309
]


def load_suspensions():
   try:
       with open(SUSPENSION_FILE, "r") as f:
           data = f.read().strip()
           return json.loads(data) if data else {}
   except json.JSONDecodeError:
       return {}


def save_suspensions(data):
   with open(SUSPENSION_FILE, "w") as f:
       json.dump(data, f)


class Unsuspend(commands.Cog):
   def __init__(self, bot):
       self.bot = bot


@bot.tree.command(name="unsuspend", description="Unsuspend a user and restore their roles.")
@app_commands.describe(user="The user to unsuspend")
@app_commands.guilds(discord.Object(id=1311735780699537452))  # Temp: force sync to your guild
async def unsuspend(interaction: Interaction, user: discord.Member):
   if not any(role.id in ALLOWED_ROLE_IDS for role in interaction.user.roles):
       return await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)


   suspensions = load_suspensions()
   str_user_id = str(user.id)


   if str_user_id not in suspensions:
       return await interaction.response.send_message("❌ This user is not currently suspended.", ephemeral=True)


   await user.remove_roles(interaction.guild.get_role(TEMP_ROLE))
   restored_roles = [
       interaction.guild.get_role(rid)
       for rid in suspensions[str_user_id]["roles"]
       if interaction.guild.get_role(rid)
   ]


   await user.add_roles(*restored_roles)


   log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
   if log_channel:
       embed = Embed(title="🔓 User Unsuspended", color=0x00ff00)
       embed.add_field(name="User", value=user.mention, inline=False)
       embed.add_field(name="By", value=interaction.user.mention, inline=False)
       embed.set_footer(text=f"User ID: {user.id}")
       await log_channel.send(embed=embed)


   del suspensions[str_user_id]
   save_suspensions(suspensions)


   await interaction.response.send_message(f"{user.mention} has been unsuspended and their roles restored ✅", ephemeral=True)








#####
# FEEDBACK
#1352020648272203827


FEEDBACK_CHANNEL_ID = 1352020648272203827




@bot.tree.command(name="feedback-submit", description="Submit feedback about a staff member.")
@app_commands.describe(
   user="The LASD member you're giving feedback about",
   rating="Rating from 1 to 10",
   feedback="Your feedback message"
)
@app_commands.choices(
   rating=[
       app_commands.Choice(name=str(i), value=i) for i in range(1, 11)
   ]
)
@app_commands.guilds(discord.Object(id=1311735780699537452))
async def feedback_submit(interaction: Interaction, user: User, rating: app_commands.Choice[int], feedback: str):
   embed = Embed(
       title="Deputy Feedback",
       color=0x3b0a08
   )
   embed.set_author(
       name=f"Submitted by {interaction.user.display_name}",
       icon_url=interaction.user.avatar.url if interaction.user.avatar else None
   )
   embed.add_field(name="Deputy", value=user.mention, inline=True)
   embed.add_field(name="Rating", value=f"{'⭐' * rating.value} ({rating.value}/10)", inline=True)
   embed.add_field(name="Feedback", value=feedback, inline=False)
   embed.add_field(name=f"Submitted by", value=f"{interaction.user.mention}", inline=True)
   embed.set_footer(text=f"Use the `/feedback-submit` command to submit feedback.")




   channel = bot.get_channel(FEEDBACK_CHANNEL_ID)
   if channel:
       await channel.send(content=user.mention, embed=embed)


   try:
       await interaction.user.send("✅ Your feedback was submitted.")
   except:
       pass


   await interaction.response.send_message("Thank you for your feedback!", ephemeral=True)






@bot.event
async def on_ready():
   guild = discord.Object(id=1311735780699537452)
   synced = await bot.tree.sync(guild=guild)
   print(f"✅ Synced {len(synced)} commands.")









#### Resignation

ALLOWED_ROLE_IDS = [
    1395826104136110211,
    1316556364285218827,
    1354280877646942309,
    1388243019437838437,
    1340506488187392080,
    1311735780783292477,
    1311735780766646393,
]

@bot.tree.command(name="resignation-log", description="Log a resignation.")
@app_commands.describe(
    user="The user who resigned",
    role="Their former role/title"
)
@app_commands.guilds(discord.Object(id=1311735780699537452))  # Optional for faster sync
async def resignation_log(interaction: discord.Interaction, user: discord.User, role: discord.Role):
    LOG_CHANNEL_ID = 1339025179833143417  # Replace with your log channel ID

    # Restrict usage to certain role IDs
    if not any(role.id in ALLOWED_ROLE_IDS for role in interaction.user.roles):
        return await interaction.response.send_message(
            "❌ You do not have permission to use this command.", ephemeral=True
        )

    embed = discord.Embed(
        title="📄 Resignation Logged",
        description=(
            f"We regret to inform you that {user.mention} has resigned from their position as **@{role}**.\n"
            f"We appreciate the work they contributed during their time with us and thank them for their efforts."
        ),
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="User", value=f"{user.mention} (`{user.id}`)", inline=False)
    embed.add_field(name="Former Role", value=role, inline=False)
    embed.add_field(name="Logged By", value=interaction.user.mention, inline=False)
    embed.set_footer(text="Resignation System")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1341068775868469309/1399438086018175016/out.png?ex=6888ffc8&is=6887ae48&hm=fa0dc18d8550f0f7d21a7b338268abb8f458b9bbde42509dc2fdf30b9cd7a3ff&")

    channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(content=user.mention, embed=embed)
        await interaction.response.send_message(
            f"✅ Resignation logged for {user.mention} as {role}.", ephemeral=True
        )
    else:
        await interaction.response.send_message("❌ Log channel not found.", ephemeral=True)

bot.run(TOKEN)





