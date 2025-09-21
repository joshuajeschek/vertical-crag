import argparse
import server

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      prog='vertical-crag',
      description='Automatically add routes to thecrag.com')
  subparsers = parser.add_subparsers()
  server_parser = subparsers.add_parser('server')
  server_parser.set_defaults(func=server.run)

  args = parser.parse_args()
  args.func(args)
