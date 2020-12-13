from src.team_maker.team_maker import TeamMaker
from discord.ext import commands
from ..embed_builder import Embed_Builder

class CommandsCog(commands.Cog):
    """
    基本的なコマンド
    """
    def __init__(self, bot) -> None:
        self.bot = bot
        self.tm: TeamMaker = bot.tm

    @commands.command()
    async def add(self, ctx, *names: str) -> None:
        """
        Botに名前を追加して、結果を表示する
        """
        # 名前が入力されていない場合その旨を出力する
        if len(names) == 0:
            await ctx.send("名前が入力されていません")
            return

        # メンバーの追加を試み、追加したメンバーとしていないメンバーに分ける
        added_members = []
        for name in names:
            try:
                self.tm.add_member(name)
                added_members.append(name)
            except ValueError:
                pass
        
        # 一人も追加しなかった場合その旨を出力して終了
        if len(added_members) == 0:
            await ctx.send("追加したメンバーはありません")
            return

        # Discordに表示される埋め込みオブジェクトの作成と送信
        eb = Embed_Builder("追加")
        eb.add_values("追加したメンバー", added_members)
        await ctx.send(embed=eb.embed)
    
    @commands.command(name="join")
    async def _join(self, ctx) -> None:
        """
        Botに送信者の名前を追加して、結果を表示する
        """
        
        name = ctx.author.display_name

        try:
            self.tm.add_member(name)
        except ValueError:
            await ctx.send(f"{name} は既に追加されています")
            return

        await ctx.send(f"{name} を追加しました")

    @commands.command()
    async def delete(self, ctx, *names: str) -> None:
        """
        Botに名前を追加して結果を表示する
        """
        # 名前が入力されていない場合その旨を出力して終了
        if len(names) == 0:
            await ctx.send("名前が入力されていません")
            return

        # メンバーの追加を試み、追加したメンバーとしていないメンバーに分ける
        deleted_members = []
        for name in names:
            try:
                self.tm.delete_member(name)
                deleted_members.append(name)
            except ValueError:
                pass

        # 一人も削除しなかった場合その旨を出力して終了
        if len(deleted_members) == 0:
            await ctx.send("削除したメンバーはありません")
            return

        # Discordに表示される埋め込みオブジェクトの作成と送信
        eb = Embed_Builder("削除")
        eb.add_values("削除したメンバー", deleted_members)
        await ctx.send(embed=eb.embed)

    @commands.command()
    async def leave(self, ctx) -> None:
        """
        Botから送信者の名前を削除して、結果を表示する
        """
        
        name = ctx.author.display_name

        try:
            self.tm.delete_member(name)
        except ValueError:
            await ctx.send(f"{name} は追加されていません")
            return

        await ctx.send(f"{name} を削除しました")

    @commands.command()
    async def clear(self, ctx) -> None:
        """
        チームメーカーにのメンバーを全て削除する
        """
        self.tm.clear_member()
        await ctx.send("全てのメンバーを削除しました")

    @commands.command(name="list")
    async def _list(self, ctx) -> None:
        """
        チームメーカーに追加済みのメンバーを表示する
        """
        members = self.tm.members
        
        # メンバーが登録されていない場合その旨を出力して終了
        if len(members) == 0:
            await ctx.send("メンバーが登録されていません")
            return
        
        # Discordに表示される埋め込みオブジェクトの作成と送信
        eb = Embed_Builder("表示")
        eb.add_values("追加済みのメンバー", members)
        await ctx.send(embed=eb.embed)

    @commands.command()
    async def make(self, ctx) -> None:
        """
        チーム分けをして表示する
        """
        # メンバーがチーム数より少ない場合その旨を出力して終了
        if len(self.tm.members) < self.tm.team_num:
            await ctx.send("メンバーが少なすぎます")
            return
        
        # チーム分け
        self.tm.make_team()

        # Discordに表示される埋め込みオブジェクトの作成と送信
        eb = Embed_Builder("チーム分け")
        # チームに分けられたメンバー
        for i, team in enumerate(self.tm.teams):
            eb.add_values(f"チーム{i+1}", team)
        # 余りのメンバー
        if len(self.tm.remainder) > 0:
            eb.add_values("余り", self.tm.remainder, inline=False)
        await ctx.send(embed=eb.embed)

    @commands.command()
    async def addvc(self, ctx) -> None:
        """
        コマンド送信者と同じボイスチャンネルに接続している人をBotに追加して、結果を表示する
        """
        # 送信者が接続しているボイスチャンネル
        voice = ctx.author.voice

        # ボイスチャンネルに接続中でない場合、その旨を送信し終了
        if not voice:
            await ctx.send("ボイスチャンネルに入って実行してください")
            return

        # ボイスチャンネルに接続中のメンバーの表示名
        names = [member.display_name for member in voice.channel.members]

        # メンバーの追加を試み、追加したメンバーとしていないメンバーに分ける
        added_members = []
        for name in names:
            try:
                self.tm.add_member(name)
                added_members.append(name)
            except ValueError:
                pass
        
        # 一人も追加しなかった場合その旨を出力して終了
        if len(added_members) == 0:
            await ctx.send("追加したメンバーはありません")
            return

        # Discordに表示される埋め込みオブジェクトの作成と送信
        eb = Embed_Builder("追加")
        eb.add_values("追加したメンバー", added_members)
        await ctx.send(embed=eb.embed)

    @commands.command()
    async def makevc(self, ctx) -> None:
        """
        チームメーカーのメンバーを全て削除した後、
        コマンド送信者と同じボイスチャンネルに接続している人をBotに追加して、チーム分けをし、結果を表示する
        """
        # 送信者が接続しているボイスチャンネル
        voice = ctx.author.voice

        # ボイスチャンネルに接続中でない場合、その旨を送信し終了
        if not voice:
            await ctx.send("ボイスチャンネルに入って実行してください")
            return
        
        # ボイスチャンネルに接続中のメンバーの表示名
        names = [member.display_name for member in voice.channel.members]

        # メンバーがチーム数より少ない場合その旨を出力して終了
        if len(names) < self.tm.team_num:
            await ctx.send("メンバーが少なすぎます")
            return

        # メンバーを空にする
        self.tm.clear_member()

        # メンバーの追加
        for name in names:
            try:
                self.tm.add_member(name)
            except ValueError:
                pass
        
        # チーム分け
        self.tm.make_team()

        # Discordに表示される埋め込みオブジェクトの作成と送信
        eb = Embed_Builder("チーム分け")
        # チームに分けられたメンバー
        for i, team in enumerate(self.tm.teams):
            eb.add_values(f"チーム{i+1}", team)
        # 余りのメンバー
        if len(self.tm.remainder) > 0:
            eb.add_values("余り", self.tm.remainder, inline=False)
        await ctx.send(embed=eb.embed)

    @commands.command()
    async def tnum(self, ctx, num: str) -> None:
        """
        チーム数を変更する
        """
        try:
            num = int(num)
        except ValueError:
            await ctx.send("整数を入力してください")
            return
        
        if num < 2:
            await ctx.send("値が小さすぎます")

        self.tm.team_num = num

        await ctx.send(f"チーム数を {num} に変更しました")
    
    @commands.command()
    async def tsize(self, ctx, size: str) -> None:
        """
        1チームの人数を変更する
        """
        try:
            size = int(size)
        except ValueError:
            await ctx.send("整数を入力してください")
            return
        
        if size < 2:
            await ctx.send("値が小さすぎます")

        self.tm.team_size = size

        await ctx.send(f"1チームの人数を {size} に変更しました")


# Bot本体側からコグを読み込む際に呼び出される関数
def setup(bot):
    bot.add_cog(CommandsCog(bot))