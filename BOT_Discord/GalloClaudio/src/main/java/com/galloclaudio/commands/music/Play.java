package com.galloclaudio.commands.music;

import com.galloclaudio.ICommand;
import com.galloclaudio.lavaplayer.PlayerManager;
import net.dv8tion.jda.api.entities.GuildVoiceState;
import net.dv8tion.jda.api.entities.Member;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.OptionData;

import java.io.File;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;

public class Play implements ICommand {
    @Override
    public String getName() {
        return "play";
    }

    @Override
    public String getDescription() {
        return "Will play a song";
    }

    @Override
    public List<OptionData> getOptions() {
        List<OptionData> options = new ArrayList<>();
        options.add(new OptionData(OptionType.STRING, "nombre", "Name of the song to play", true));
        return options;
    }

    @Override
    public void execute(SlashCommandEvent event) {
        Member member = event.getMember();
        GuildVoiceState memberVoiceState = member.getVoiceState();

        if (!memberVoiceState.inVoiceChannel()) {
            event.reply("Pero tení que estar en un canal de voz po aweonao").queue();
            return;
        }

        Member self = event.getGuild().getSelfMember();
        GuildVoiceState selfVoiceState = self.getVoiceState();

        if (!selfVoiceState.inVoiceChannel()) {
            event.getGuild().getAudioManager().openAudioConnection(memberVoiceState.getChannel());
        } else {
            if (selfVoiceState.getChannel() != memberVoiceState.getChannel()) {
                event.reply("You need to be in the same channel as me").queue();
                return;
            }
        }

///        String nombre = event.getOption("nombre") != null ? event.getOption("nombre").getAsString() : null;
///        if (nombre == null) {
///            event.reply("Error: no se especificó el nombre de la canción").queue();
///            return;
///        }
        String nombre = "https://www.youtube.com/watch?v=pGwzgcci7tw";
        File file = new File(nombre);
        if (file.exists()) {
            // Play a local file
            PlayerManager playerManager = PlayerManager.get();
            event.reply("Playing").queue();
            playerManager.play(event.getGuild(), String.valueOf(file));
        } else {
            // Play a URL or search term
            try {
                new URI(nombre);
            } catch (URISyntaxException e) {
                nombre = "ytsearch:" + nombre;
            }

            PlayerManager playerManager = PlayerManager.get();
            event.reply("Playing").queue();
            playerManager.play(event.getGuild(), nombre);
        }
    }}