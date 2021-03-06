from src.team_maker.team_maker import TeamMaker
from discord import Member
from discord.ext import commands
from ..embed_builder import Embed_Builder

class UserSettings(commands.Cog):
    """
    設定
    """
    def __init__(self, bot) -> None:
        self.bot = bot
        self.tm: TeamMaker = bot.tm
    
    @commands.command()
    async def fix(self, ctx: commands.Context, *members: Member) -> None:
        """
        指定したメンバーが余りにならないようにする
        """
        # 名前が入力されていない場合その旨を出力する
        if len(members) == 0:
            await ctx.send("名前が入力されていません")
            return

        # メンバーの固定を試み、固定したメンバーとしていないメンバーに分ける
        fixed_members = []
        for member in members:
            try:
                self.tm.fix(member.id)
                fixed_members.append(member.display_name)
            except ValueError:
                pass
        
        # 一人も固定しなかった場合その旨を出力して終了
        if len(fixed_members) == 0:
            await ctx.send("固定したメンバーはありません")
            return

        # Discordに表示される埋め込みオブジェクトの作成と送信
        eb = Embed_Builder("固定")
        eb.add_values("固定したメンバー", fixed_members)
        await ctx.send(embed=eb.embed)
    
    @commands.command()
    async def unfix(self, ctx: commands.Context, *members: Member) -> None:
        """
        指定したメンバーの固定状態を解除する
        """
        # 名前が入力されていない場合その旨を出力する
        if len(members) == 0:
            await ctx.send("名前が入力されていません")
            return

        # メンバーの固定の解除を試み、固定を解除したメンバーとしていないメンバーに分ける
        unfixed_members = []
        for member in members:
            try:
                self.tm.unfix(member.id)
                unfixed_members.append(member.display_name)
            except ValueError:
                pass
        
        # 一人も固定解除しなかった場合その旨を出力して終了
        if len(unfixed_members) == 0:
            await ctx.send("固定を解除したメンバーはありません")
            return

        # Discordに表示される埋め込みオブジェクトの作成と送信
        eb = Embed_Builder("固定を解除")
        eb.add_values("固定を解除したメンバー", unfixed_members)
        await ctx.send(embed=eb.embed)

# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
    bot.add_cog(UserSettings(bot))