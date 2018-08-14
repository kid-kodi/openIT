# openIT
télécharger l'application en suivant les instructions suivante :
1) ouvrer l'invite de commande dans le repertoire ou vous souhaitez installer l'application
2) entrer la commande suivante git clone https://github.com/kid-kodi/openIT.git
3) lorsque le téléchargement est terminé faite 'cd openIT'
NB : ainsi vous serez à l'interieur du dossier de l'application.

si vous avez pas encore installé docker veuillez l'installer.

4) entrer la commande suivante "docker build -t openit:latest" .
5) verifier que les images suivantes ont été bien crées en entrant dans l'invite de commande
"docker images"
6) Pour lancer l'application entrer "docker run --name openit -d -p 8000:5000 --rm openit:latest" dans l'invite de commande
