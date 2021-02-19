from .card import Card
from .colours import *
from .fonts import dinpro_fonts, champions_fonts


# dictionary which maps a card code to a card object
cardcode_to_card = {

    # Top Tier
    'FREEZE': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/current_templates/Freeze.png', (WHITE, WHITE), dinpro_fonts),
    # Runner Up Tier
    'HEADLINERS': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/current_templates/Headliners.png', (WHISPER, WHISPER), dinpro_fonts),
    # Gold Tier
    'GOLD': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/current_templates/Gold.png', (BLACK, BLACK), dinpro_fonts),
    # Silver Tier 
    'SILVER': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/current_templates/Silver.png', (BLACK, BLACK), dinpro_fonts),
    # Bronze Tier
    'BRONZE': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/current_templates/Bronze.png', (BLACK, BLACK), dinpro_fonts),

    # Other 
    'FLASHBACK': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/current_templates/Flashback.png', (WHITE, WHITE), dinpro_fonts),
    'EUROPA': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/current_templates/Europa.png', (WHITE, WHITE), dinpro_fonts),
    'SUDAMERICA': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/current_templates/Sudamerica.png', (WHITE, WHITE), dinpro_fonts),
    'RULEBREAKER': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/current_templates/Rulebreaker.png', (WHITE, WHITE), dinpro_fonts),
    'FUTURE STARS': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/current_templates/Future Stars.png', (WHITE, WHITE), dinpro_fonts),


    # # Bronze
    # 'COMMON_BRONZE': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/common_bronze.png', (COMMON_BRONZE, COMMON_BRONZE), dinpro_fonts),
    # 'COMMON_SILVER': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/common_silver.png', (COMMON_SILVER, COMMON_SILVER), dinpro_fonts),
    # 'COMMON_GOLD': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/common_gold.png', (COMMON_GOLD, COMMON_GOLD), dinpro_fonts),
    # # Silver
    # 'RARE_BRONZE': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/rare_bronze.png', (RARE_BRONZE, RARE_BRONZE), dinpro_fonts),
    # 'RARE_SILVER': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/rare_silver.png', (RARE_SILVER, RARE_SILVER), dinpro_fonts),
    # 'RARE_GOLD': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/rare_gold.png', (RARE_GOLD, RARE_GOLD), dinpro_fonts),
    # # Gold
    # 'IF_BRONZE': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/if_bronze.png', (IF_BRONZE, IF_BRONZE), dinpro_fonts),
    # 'IF_SILVER': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/if_silver.png', (IF_SILVER, IF_SILVER), dinpro_fonts),
    # 'IF_GOLD': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/if_gold.png', (IF_GOLD, IF_GOLD), dinpro_fonts),
    # # FUT Champions
    # 'FC_BRONZE': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/champion_bronze.png', (FC_BRONZE, FC_BRONZE), dinpro_fonts),
    # 'FC_SILVER': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/champion_silver.png', (FC_SILVER, FC_SILVER), dinpro_fonts),
    # 'FC_GOLD': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/champion_gold.png', (FC_GOLD, FC_GOLD), dinpro_fonts),
    # # MOTM / POTM
    # 'MOTM': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/motm.png', (WHISPER, WHISPER), dinpro_fonts),
    # 'PL_POTM': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/potm_pl.png', (PL_POTM, PL_POTM), dinpro_fonts),
    # 'BL_POTM': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/potm_bundesliga.png', (BUNDESLIGA_POTM, BUNDESLIGA_POTM), dinpro_fonts),
    # # FUTTIES
    # 'FUTTIES': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/futties.png', (FUTTIES, FUTTIES), dinpro_fonts),
    # 'FUTTIESW': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/futties_winner.png', (FUTTIES, FUTTIES), dinpro_fonts),
    # # TOTY
    # 'TOTY': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/toty.png', (PORTICA, PORTICA), dinpro_fonts),
    # 'TOTY_N': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/toty_nominees.png', (PORTICA, PORTICA), dinpro_fonts),
    # # Europa League
    # 'EL': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/europa_league.png', (TANGERINE, TANGERINE), dinpro_fonts),
    # 'EL_MOTM': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/europa_league_motm.png', (WHITE_SMOKE, BLACK), dinpro_fonts),
    # 'EL_LIVE': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/europa_league_live.png', (TANGERINE, TANGERINE), dinpro_fonts),
    # 'EL_SBC': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/europa_league_sbc.png', (BLACK, BLACK), dinpro_fonts),
    # 'EL_TOTT': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/europa_league_tott.png', (WHITE_SMOKE, WHITE_SMOKE), dinpro_fonts),
    # # Champions League
    # 'COMMON_UCL': Card.factory('FIFA19_UCL', 'assets/playercard_setup/cards/original_cards/ucl_common.png', (WHISPER, WHISPER), champions_fonts),
    # 'RARE_UCL': Card.factory('FIFA19_UCL', 'assets/playercard_setup/cards/original_cards/ucl_rare.png', (WHISPER, WHISPER), champions_fonts),
    # 'UCL_MOTM': Card.factory('FIFA19_UCL', 'assets/playercard_setup/cards/original_cards/ucl_motm.png', (WHISPER, WHISPER), champions_fonts),
    # 'UCL_LIVE': Card.factory('FIFA19_UCL', 'assets/playercard_setup/cards/original_cards/ucl_live.png', (WHISPER, WHISPER), champions_fonts),
    # 'UCL_SBC': Card.factory('FIFA19_UCL', 'assets/playercard_setup/cards/original_cards/ucl_sbc.png', (WHISPER, WHISPER), champions_fonts),
    # 'UCL_TOTT': Card.factory('FIFA19_UCL', 'assets/playercard_setup/cards/original_cards/ucl_tott.png', (WHISPER, WHISPER), champions_fonts),
    # # FUT Swap
    # 'FSR': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/fut_swap_rewards.png', (FUT_SWAP_REWARDS, FUT_SWAP_REWARDS), dinpro_fonts),
    # # Future Stars
    # 'FS': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/future_stars.png', (FUTURE_STARS, FUTURE_STARS), dinpro_fonts),
    # 'FSN': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/future_stars_nominees.png', (FUTURE_STARS, FUTURE_STARS), dinpro_fonts),
    # # MISC
    # 'PP': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/pro_player.png', (WHISPER, WHISPER), dinpro_fonts),
    # 'CB': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/carniball.png', (BRAZILIAN_YELLOW, BRAZILIAN_YELLOW), dinpro_fonts),
    # 'RB': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/record_breaker.png', (SPRING_BUD, SPRING_BUD), dinpro_fonts),
    # 'HERO': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/hero.png', (PHOCA, PHOCA), dinpro_fonts),
    # 'AW': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/award_winner.png', (AWARD_WINNER, AWARD_WINNER), dinpro_fonts),
    # 'FB': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/flashback.png', (FLASHBACK, FLASHBACK), dinpro_fonts),
    # 'HEADLINERS': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/headliners.png', (WHISPER, WHISPER), dinpro_fonts),
    # # 'CC': Card.factory('FIFA19_STD', 'assets/19/cards/concept.png', (CONCEPT, CONCEPT), dinpro_fonts),
    # 'SBC': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/sbc.png', (SQUAD_BUILDER, SQUAD_BUILDER), dinpro_fonts),
    # 'SBCP': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/sbc_premium.png', (SQUAD_BUILDER_PREMIUM, SQUAD_BUILDER_PREMIUM), dinpro_fonts),
    # 'LEGEND': Card.factory('FIFA19_STD', 'assets/playercard_setup/cards/original_cards/legend.png', (LEGEND, LEGEND), dinpro_fonts)

}

