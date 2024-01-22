import src.util.argparser as parser
import src.util.scheduler as scheduler


def main():
    args = parser.get_parser().parse_args()
    scheduler.scheduler(args)
    return


if __name__ == '__main__':
    main()
