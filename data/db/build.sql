CREATE TABLE IF NOT EXISTS guilds (
        GuildID integer PRIMARY KEY,
        Prefix text DEFAULT "poo."
);

CREATE TABLE IF NOT EXISTS modusage (
        daysSinceFunny integer,
        dateOfFunny date
);