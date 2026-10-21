"""Desktop launcher; user saves remain outside bundled application files."""
import argparse, os, sqlite3, sys, threading, webbrowser
from pathlib import Path
import server

def data_dir():
 base=Path(os.environ.get('LOCALAPPDATA',str(Path.home()/'.local'/'share')))
 return base/'THORNS'
def migrate(destination,source):
 if destination.exists() or not source.exists():return False
 destination.parent.mkdir(parents=True,exist_ok=True)
 # Exclusive reservation prevents replacing an existing destination.
 try:destination.touch(exist_ok=False)
 except FileExistsError:return False
 try:
  with sqlite3.connect(source) as src,sqlite3.connect(destination) as dst:src.backup(dst)
 except Exception:
  destination.unlink(missing_ok=True);raise
 return True
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765);parser.add_argument('--host',default='0.0.0.0');parser.add_argument('--no-browser',action='store_true');args=parser.parse_args()
 folder=data_dir();folder.mkdir(parents=True,exist_ok=True);db=folder/'thorns-saves.sqlite3'
 legacy=(Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).parent)/'thorns-saves.sqlite3'
 migrate(db,legacy);server.init_db(str(db))
 try:http=server.ThreadingHTTPServer((args.host,args.port),server.Handler)
 except OSError as exc:
  server.DB.close();raise SystemExit(f'Cannot start THORNS: {exc}. Close another instance or choose --port 8766.')
 print(f'THORNS: http://localhost:{args.port}\nSaves: {db}\nKeep this window open. Ctrl+C stops the server.',flush=True)
 if not args.no_browser:threading.Timer(0.5,lambda:webbrowser.open(f'http://localhost:{args.port}')).start()
 try:http.serve_forever()
 except KeyboardInterrupt:pass
 finally:http.server_close();server.DB.close()
if __name__=='__main__':main()
