/* the sample vault: nine short notes in three areas (operations, audio, control) plus a cache policy that was reversed.
   Every claim line is "subject relation object"; wikilinks are [[note]]. */
const VAULT = {
 'circuit-breaker': `# Circuit breaker
tags: ops
Stops calling a service that keeps failing, so the service gets room to recover.
- circuit_breaker prevents cascade_failure
- cascade_failure causes outage
See also [[retry-storm]].`,
 'retry-storm': `# Retry storm
tags: ops
After a hiccup every client retries at once; the extra load keeps the service down, which causes more retries.
- retry_storm is positive_feedback
- retry_storm causes overload
- overload causes outage`,
 'microphone-squeal': `# Microphone squeal
tags: audio
The microphone hears the speaker, the amplifier makes it louder, the speaker gets louder still, and the howl grows.
- microphone_squeal is positive_feedback
- positive_feedback causes runaway_growth
- microphone_squeal causes ringing_noise`,
 'thermostat': `# Thermostat
tags: control
A heater switches off when the room is warm enough, so the temperature settles near the target.
- thermostat uses negative_feedback
- negative_feedback prevents runaway_growth
- negative_feedback causes stability`,
 'resonance': `# Resonance
tags: control
Push a swing at its natural rhythm and each push adds to the last one, so the swing goes higher and higher.
- resonance causes runaway_growth
- resonance needs matched_rhythm`,
 'counterpoint': `# Counterpoint
tags: music
Melodies that move on their own paths yet sound good together. The rules keep each voice independent.
- counterpoint needs voice_independence
- parallel_fifths breaks voice_independence`,
 'parallel-fifths': `# Parallel fifths
tags: music
Two voices that move together a fifth apart sound like one voice, so the music loses its independence.
- parallel_fifths breaks voice_independence
- parallel_fifths causes thin_texture`,
 'cache-ttl-2023': `# Cache time to live (2023)
tags: ops
Keep entries for a long time to save work.
- long_ttl prevents stale_reads
- long_ttl causes fast_reads`,
 'cache-ttl-2024': `# Cache time to live (2024)
tags: ops
We were wrong in 2023: a long time to live serves old data. Use a short one. This replaces [[cache-ttl-2023]].
- long_ttl causes stale_reads
- cache-ttl-2024 supersedes cache-ttl-2023`,
 'retry-advice-alice': `# Retry advice (Alice)
tags: ops
Retry again straight away; the sooner the call goes through, the shorter the trouble.
- fast_retry prevents outage`,
 'retry-advice-bob': `# Retry advice (Bob)
tags: ops
Do not retry straight away: a quick retry from every client piles on the extra load.
- fast_retry causes outage`,
};
