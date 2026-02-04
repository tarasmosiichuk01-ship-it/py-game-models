import json

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json") as file:
        data = json.load(file)

    for nickname, player_data in data.items():

        race_data = player_data.get("race")
        if race_data:
            race_name = race_data.get("name")
            race_description = race_data.get("description")
            race, created = Race.objects.get_or_create(
                name=race_name,
                defaults={"description": race_description}
            )

            race_skills = race_data.get("skills")
            if race_skills:
                for race_skill in race_skills:
                    skill, created = Skill.objects.get_or_create(
                        name=race_skill.get("name"),
                        race=race,
                        defaults={"bonus": race_skill.get("bonus")}
                    )

        guild_data = player_data.get("guild")
        if guild_data:
            guild, created = Guild.objects.get_or_create(
                name=guild_data.get("name"),
                defaults={"description": guild_data.get("description")}
            )
        else:
            guild = None

        Player.objects.create(
            nickname=nickname,
            email=player_data.get("email"),
            bio=player_data.get("bio"),
            race=race,
            guild=guild
        )

if __name__ == "__main__":
    main()
