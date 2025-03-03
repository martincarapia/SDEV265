# Risk-it Ralph

Risk-it Ralph is a Discord Bot that aims to bring more fun, excitement, and friendly competition to your Discord server!

Although in the early stages of development and without any code scripted yet, this project will offer a variety of gambling-type and casino-style games. It will allow users to bet, wager, win, and lose virtual currency in a safe, non-harmful, and family-friendly way.

This project, centered around the Python programming language, will feature the following:

* Classic casino games like Blackjack, Roulette, and Slots.
* A custom currency system where players can earn and wager tokens.
* Leaderboards and achievements to show off your winning streaks.
* Fun and engaging commands for your server to enjoy.

## Developers

Clone the project from GitHub and navigate into the directory:

```bash
git clone https://github.com/martincarapia/SDEV265.git
cd SDEV265
```

You'll need to have Python 3.10 or above:

```bash
python --version
```

It's recommended to use a virtual environment for Python projects to avoid package dependency issues:

```bash
python -m venv venv
```

Activate the virtual environment:

On Windows:
```bash
.\venv\Scripts\activate
```

On macOS and Linux:
```bash
source venv/bin/activate
```

Your terminal prompt should now indicate that the virtual environment is active. You can now install your project dependencies within this isolated environment:

```bash
pip install -r requirements.txt
```

You'll need to create a `.env` file with a Discord bot token to run the code:

```bash
echo 'TOKEN=YOURTOKENSTRINGVALUE' >> src/.env
```

You can learn how to set up a Discord application [here](https://docs.discord4j.com/discord-application-tutorial).

Once your requirements are installed and you have a valid token in your `.env` file, run `main.py`:

```bash
python src/main.py
```

Your terminal output should look something like this, and your bot should be online in the server you invited it to:

```bash
(venv) (base) example@computer SDEV265 % python src/main.py 
2025-03-03 09:37:16 INFO     discord.client logging in using static token
2025-03-03 09:37:16 INFO     discord.gateway Shard ID None has connected to Gateway (Session ID: b530911fd5e359cb584c380276815754).
Logged in as RiskItRalphDEVSERVE#2356!
```
