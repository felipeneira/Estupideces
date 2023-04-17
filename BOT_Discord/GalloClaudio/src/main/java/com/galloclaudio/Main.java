package com.galloclaudio;

import com.galloclaudio.commands.music.NowPlaying;
import com.galloclaudio.commands.music.Play;
import com.galloclaudio.commands.music.Queue;
import com.galloclaudio.commands.music.Repeat;
import com.galloclaudio.commands.music.Skip;
import com.galloclaudio.commands.music.Stop;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;

import javax.security.auth.login.LoginException;

public class Main {

    public static void main(String[] args) throws LoginException {
        JDA jda = JDABuilder.createDefault("MTA4Njc0MDQ2NjE5Nzg3Njk1OQ.GJHbdU.gBerpxBj2JB3fWSYovO2Qtvto_VsSdEUovaVFY").build();
        CommandManager manager = new CommandManager();
        manager.add(new Play());
        manager.add(new Skip());
        manager.add(new Stop());
        manager.add(new NowPlaying());
        manager.add(new Queue());
        manager.add(new Repeat());
        jda.addEventListener(new SlashCommandListener(manager));
    }
}
