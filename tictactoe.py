import click

from objects.gameObjects import Token
from objects.playerviewcontroller import GameController
from utils.graph_utils import write_graph, search_all_boards
from configurations import playerTypes, viewTypes

@click.command()
@click.option("--writegraph", is_flag=True, type=click.BOOL, default=False)
@click.option("--playcross", is_flag=True, type=click.BOOL, default=False)
@click.option("--twoplayer", is_flag=True, type=click.BOOL, default=False)
@click.option("--boteasy", is_flag=True, type=click.BOOL, default=False)
@click.option("--bothard", is_flag=True, type=click.BOOL, default=False)
@click.option("--optimallybad", is_flag=True, type=click.BOOL, default=False)
@click.option("--menace", is_flag=True, type=click.BOOL, default=False)
def main(writegraph, playcross, twoplayer, boteasy, bothard, optimallybad, menace):
    if writegraph:
        write_graph(search_all_boards())

    human = Token.NAUGHT
    other = Token.CROSS 
    if playcross or menace:
        other = Token.NAUGHT 
        human = Token.CROSS

    if menace:
        players = {
            human: playerTypes.HumanTerminalPlayer(human),
            other: playerTypes.MENACEPlayer(other)
        }
    elif twoplayer:
        players = {
            human: playerTypes.HumanTerminalPlayer(human),
            other: playerTypes.HumanTerminalPlayer(other)
        }
    elif boteasy:
        players = {
            human: playerTypes.HumanTerminalPlayer(human),
            other: playerTypes.RandomAIPlayer(other)
        }
    elif bothard:
        players = {
            human: playerTypes.HumanTerminalPlayer(human),
            other: playerTypes.SmartAIPlayer(other)
        }
    elif optimallybad:
        players = {
            human: playerTypes.HumanTerminalPlayer(human),
            other: playerTypes.OptimallyBadAIPlayer(other)
        }
    else:  # bothard by default
        players = {
            human: playerTypes.HumanTerminalPlayer(human),
            other: playerTypes.SmartAIPlayerRework(other)
        }

    while True:
        controller = GameController(players, viewTypes.TerminalBoardView)
        controller.runGame()

        response = input("Play again? ")
        if response.lower() in ("no", "n", "stop", "break", "exit", "-1"):
            break


if __name__ == "__main__":
    main()
