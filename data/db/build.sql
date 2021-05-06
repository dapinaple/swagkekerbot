CREATE TABLE IF NOT EXISTS guilds (
        GuildID integer PRIMARY KEY,
        Prefix text DEFAULT "poo.",
        ghostID integer 

);

CREATE TABLE IF NOT EXISTS modusage (
        daysSinceFunny integer,
        dateOfFunny date

);