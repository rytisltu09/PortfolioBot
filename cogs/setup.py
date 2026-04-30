from discord.ext import commands
import discord
import datetime


import datetime
import discord

class SetupDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Minimal Setup",
                description="Only logging channel."
            ),
            discord.SelectOption(
                label="Standard Setup",
                description="Logging + AutoMod."
            ),
            discord.SelectOption(
                label="Maximalist Setup",
                description="Everything enabled."
            )
        ]
        super().__init__(
            placeholder="Choose your setup option",
            options=options,
            custom_id="setup_dropdown"
        )

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]

        if selected == "Minimal Setup":
            channel = await create_logging(interaction.guild)
            await interaction.response.send_message(
                f"✅ Minimal setup complete.\nCreated: {channel.mention}",
                ephemeral=True
            )

        elif selected == "Standard Setup":
            await setup_automod(interaction.guild)
            channel = await create_logging(interaction.guild)
            await interaction.response.send_message(
                f"✅ Standard setup complete.\nCreated: {channel.mention}",
                ephemeral=True
            )

        elif selected == "Maximalist Setup":
            await setup_automod(interaction.guild)
            channel = await create_logging(interaction.guild)
            joins = await create_joins(interaction.guild)
            await interaction.response.send_message(
                f"✅ Maximalist setup complete.\nCreated: {channel.mention}, {joins.mention}",
                ephemeral=True
            )

async def setup_automod(guild: discord.Guild):
    # Bad words filter, more words can be added on, a .txt file can also be used to replace the list.
    try:
        await guild.create_automod_rule(
            name="Bad Words Filter",
            event_type=discord.AutoModRuleEventType.message_send,
            trigger=discord.AutoModTrigger(
                type=discord.AutoModRuleTriggerType.keyword,
                keyword_filter=["shit", "fuck", "dick", "suck", "cum", "semen", "boobs", "boob", "tits", "titty", "titties"]
            ),
            actions=[
                discord.AutoModRuleAction(
                    type=discord.AutoModRuleActionType.block_message,
                    custom_message="Refrain from profanity."
                )
            ],
            enabled=True
        )
        # Spam Filter
        await guild.create_automod_rule(
            name="Spam Filter",
            event_type=discord.AutoModRuleEventType.message_send,
            trigger=discord.AutoModTrigger(
                type=discord.AutoModRuleTriggerType.spam
            ),
            actions=[
                discord.AutoModRuleAction(
                    type=discord.AutoModRuleActionType.block_message
                )
            ],
            enabled=True
        )
        # Mention Spam Filter
        await guild.create_automod_rule(
            name="Mention Spam Filter",
            event_type=discord.AutoModRuleEventType.message_send,
            trigger=discord.AutoModTrigger(
                type=discord.AutoModRuleTriggerType.mention_spam
            ),
            actions=[
                discord.AutoModRuleAction(
                    type=discord.AutoModRuleActionType.block_message
                ),
                discord.AutoModRuleAction(
                    type=discord.AutoModRuleActionType.timeout,
                    duration=datetime.timedelta(minutes=10)
                )
            ],
            enabled=True
        )
    except Exception as e:
        print(f"{e}")

async def create_logging(guild: discord.Guild):
    existing = discord.utils.get(guild.text_channels, name="nova-logs")
    if existing:
        return existing

    bot_member = guild.me
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        bot_member: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True
        )
    }
    channel = await guild.create_text_channel(
        name="nova-logs",
        topic="Server logs created by Nova.",
        overwrites=overwrites
    )
    return channel


async def create_joins(guild: discord.Guild):
    existing = discord.utils.get(guild.text_channels, name="joins")
    if existing:
        return existing

    bot_member = guild.me
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=True),
        bot_member: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=False
        )
    }
    channel = await guild.create_text_channel(
        name="joins",
        topic="Tracks joins for the server.",
        overwrites=overwrites
    )
    return channel

class SetupDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SetupDropdown())


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="setup",
        description="Setup Nova bot"
    )
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx: commands.Context):
        file = discord.File(
            "cogs/images/setup.png",
            filename="setup.png"
        )

        icon_url = self.bot.user.display_avatar.url

        embed = discord.Embed(
            description=(
                "## Welcome to the Nova Setup Panel.\n"
                "### Choose one of the available setup profiles below "
                "to configure your server quickly and efficiently."
            ),
            color=0x648894
        )

        embed.set_thumbnail(url="attachment://setup.png")
        embed.set_author(name="NovaAPP", icon_url=icon_url)

        embed.add_field(
            name="🔹 **Minimal Setup**",
            value="Creates a dedicated logging channel.",
            inline=False
        )

        embed.add_field(
            name="🔹 **Standard Setup (best default option)**",
            value="Creates logging + AutoMod",
            inline=False
        )

        embed.add_field(
            name="🔹 **Maximalist Setup**",
            value="Every feature from Nova.",
            inline=False
        )

        embed.add_field(
            name="📌 **Before You Continue**",
            value=(
                "*Using setup is completely optional. "
                "This feature is designed to save time by automatically configuring logging and moderation systems for your server.*"
            ),
            inline=False
        )
        embed.set_footer(text="Select a setup option from the dropdown menu below.")
        await ctx.send(
            embed=embed,
            file=file,
            view=SetupDropdownView()
        )


async def setup(bot):
    await bot.add_cog(Logging(bot))