import construct

## HEADER PACKET RECEIVED

SIZE_PACKET_CLIENT_HEADER = 0x08

PacketClientHeader = construct.Struct("PacketClientHeader",
    construct.UBInt16("sequence"),                              # + 0x00
    construct.UBInt16("session_id"),                            # + 0x02
    construct.UBInt16("unk_word_00"),                           # + 0x04
    construct.UBInt8("unk_byte_00"),                            # + 0x06
    construct.UBInt8("opcode"),                                 # + 0x07
                        )

##########################################################################

CHARACTER = construct.Struct("CHARACTER",
    construct.String("nickname", 0x18, padchar="\x00"),         # + 0x00
    construct.String("last_name", 0x18, padchar="\x00"),        # + 0x18
    construct.UBInt8("level"),                                  # + 0x30
    construct.UBInt8("career"),                                 # + 0x31
    construct.UBInt8("realm"),                                  # + 0x32
    construct.UBInt8("gender"),                                 # + 0x33
    construct.UBInt16("unk_word_00"),                           # + 0x34
    construct.ULInt16("zone"),                                  # + 0x36    /!\ Field on little endian
    construct.Array(0x0C, construct.UBInt8("unk_data_00")),     # + 0x38
    )

ABILITY_STRUCT = construct.Struct("ABILITY_STRUCT",
    construct.UBInt16("id_ability"),                            # + 0x00
    construct.UBInt8("level"),                                  # + 0x02
    )
                        
##########################################################################

## PACKET RECEIVED

# OPCODE VALUE
# SIZE PACKET
# Structure

F_PLAYER_EXIT = 0x04
SIZE_PACKET_F_PLAYER_EXIT = 4
PACKET_F_PLAYER_EXIT = construct.Struct("PACKET_F_PLAYER_EXIT",
    construct.UBInt16("session_id"),                            # + 0x00
    construct.UBInt16("unk_word_00"),                           # + 0x02
    )

F_PING = 0x0B
SIZE_PACKET_F_PING = 0x14
PACKET_F_PING = construct.Struct("PACKET_F_PING",
    construct.UBInt32("timestamp"),                             # + 0x00
    construct.UBInt32("unk_dword_00"),                          # + 0x04
    construct.UBInt32("unk_dword_01"),                          # + 0x08
    construct.UBInt16("unk_word_00"),                           # + 0x0C
    construct.UBInt16("unk_word_01"),                           # + 0x0E
    construct.UBInt16("unk_word_02"),                           # + 0x10
    construct.UBInt16("unk_word_03"),                           # + 0x12
    )

F_CONNECT = 0x0F
SIZE_PACKET_F_CONNECT = 0x88
PACKET_F_CONNECT = construct.Struct("PACKET_F_CONNECT",
    construct.UBInt8("unk_byte_00"),                            # + 0x00
    construct.UBInt8("unk_byte_01"),                            # + 0x01
    construct.UBInt8("major_version"),                          # + 0x02
    construct.UBInt8("minor_version"),                          # + 0x03
    construct.UBInt8("revision_version"),                       # + 0x04
    construct.UBInt8("unk_byte_02"),                            # + 0x05
    construct.UBInt16("unk_word_00"),                           # + 0x06
    construct.UBInt32("protocol_version"),                      # + 0x08
    construct.String("session_id", 0x65),                       # + 0x0C
    construct.String("username", 0x15),                         # + 0x71
    construct.UBInt16("size_xml"),                              # + 0x86
    )

F_OPEN_GAME = 0x17
SIZE_PACKET_F_OPEN_GAME = 0x02
PACKET_F_OPEN_GAME = construct.Struct("PACKET_F_OPEN_GAME",
    construct.UBInt8("unk_byte_00"),               # + 0x00
    construct.UBInt8("unk_byte_01"),               # + 0x01
    )

F_DUMP_ARENAS_LARGE = 0x35
SIZE_PACKET_F_DUMP_ARENAS_LARGE = 0x02
PACKET_F_DUMP_ARENAS_LARGE = construct.Struct("PACKET_F_DUMP_ARENAS_LARGE",
    construct.UBInt8("unk_byte_00"),               # + 0x00
    construct.UBInt8("unk_byte_01"),               # + 0x01
    )

F_REQUEST_CHAR = 0x54
SIZE_PACKET_F_REQUEST_CHAR = 0x3
PACKET_F_REQUEST_CHAR = construct.Struct("PACKET_F_REQUEST_CHAR",
    construct.UBInt16("command"),                               # + 0x00
    construct.UBInt8("unk_byte_00"),                            # + 0x02
    )


F_ENCRYPTKEY = 0x5C
SIZE_PACKET_F_ENCRYPTKEY = 0x06
PACKET_F_ENCRYPTKEY = construct.Struct("PACKET_F_ENCRYPTKEY",
    construct.UBInt8("key_present"),                            # + 0x00
    construct.UBInt8("unk_byte_00"),                            # + 0x01
    construct.UBInt8("major_version"),                          # + 0x02
    construct.UBInt8("minor_version"),                          # + 0x03
    construct.UBInt8("revision_version"),                       # + 0x04
    construct.UBInt8("unk_byte_01"),                            # + 0x05
                        )

F_INIT_PLAYER = 0x7C
SIZE_PACKET_F_INIT_PLAYER = 0x00000016
PACKET_F_INIT_PLAYER = construct.Struct("PACKET_F_INIT_PLAYER",
    construct.UBInt16("unk_word_00"),                           # + 0x00
    construct.UBInt16("unk_word_01"),                           # + 0x02
    construct.UBInt16("unk_word_02"),                           # + 0x04
    construct.UBInt16("unk_word_03"),                           # + 0x06
    construct.UBInt16("unk_word_04"),                           # + 0x08
    construct.UBInt16("unk_word_05"),                           # + 0x0A
    construct.UBInt16("unk_word_06"),                           # + 0x0C
    construct.UBInt16("unk_word_07"),                           # + 0x0E
    construct.UBInt8("unk_byte_00"),                            # + 0x10
    construct.Array(0x5, construct.ULInt8("unk_data_00")),      # + 0x11
    )

F_PLAYER_ENTER_FULL = 0xB8
SIZE_PACKET_F_PLAYER_ENTER_FULL = 0x30
PACKET_F_PLAYER_ENTER_FULL = construct.Struct("PACKET_F_PLAYER_ENTER_FULL",
    construct.UBInt16("unk_word_00"),                           # + 0x00
    construct.UBInt8("unk_byte_00"),                            # + 0x02
    construct.UBInt8("unk_byte_01"),                            # + 0x03
    construct.Array(0x18, construct.ULInt8("unk_data_00")),     # + 0x04
    construct.UBInt16("ns_port"),                               # + 0x1C
    construct.String("langage", 0x06),                          # + 0x1E
    construct.UBInt32("unk_dword_00"),                          # + 0x24
    construct.UBInt32("unk_dword_01"),                          # + 0x28
    construct.UBInt32("unk_dword_02"),                          # + 0x2C
                        )

F_INTERFACE_COMMAND = 0xC8
SIZE_PACKET_F_INTERFACE_COMMAND = 0x06 # MAYBE OTHER
PACKET_F_INTERFACE_COMMAND = construct.Struct("PACKET_F_INTERFACE_COMMAND",
    construct.UBInt8("unk_byte_00"),                            # + 0x00
    construct.UBInt8("unk_byte_01"),                            # + 0x01
    construct.UBInt16("unk_word_00"),                           # + 0x02
    construct.UBInt16("unk_word_01"),                           # + 0x04
    )
    
F_SWITCH_ATTACK_MODE = 0xDC
SIZE_PACKET_F_SWITCH_ATTACK_MODE = 0x04
PACKET_F_SWITCH_ATTACK_MODE = construct.Struct("PACKET_F_SWITCH_ATTACK_MODE",
    construct.UBInt8("unk_byte_00"),                            # + 0x00
    construct.Padding(3),                                       # + 0x01
    )

##########################################################################

## PACKET SENT

# OPCODE VALUE
# SIZE PACKET
# Structure

F_PLAYER_HEALTH = 0x05
SIZE_PACKET_F_PLAYER_HEALTH = 0x10
PACKET_F_PLAYER_HEALTH = construct.Struct("PACKET_F_PLAYER_HEALTH",
    construct.UBInt32("hit_points_current"),     # + 0x00
    construct.UBInt32("hit_points_max"),         # + 0x04
    construct.UBInt16("action_points_current"),  # + 0x08
    construct.UBInt16("action_points_max"),      # + 0x0A
    construct.UBInt16("unk_word_00"),            # + 0x0C
    construct.UBInt16("unk_word_01"),            # + 0x0E
    )

F_CHAT = 0x06
SIZE_PACKET_F_CHAT = 0x00
PACKET_F_CHAT = construct.Struct("PACKET_F_CHAT",
    construct.UBInt16("object_id"),              # + 0x00
    construct.UBInt8("filter"),                  # + 0x02
    construct.Padding(4),                        # + 0x03
    construct.PascalString("name_sender",
        length_field = construct.UBInt8("length")),  # + 0x..
    construct.PascalString("text",
        length_field = construct.UBInt16("length")),  # + 0x..
    )    
    
F_MAX_VELOCITY = 0x1E
SIZE_PACKET_F_MAX_VELOCITY = 0x02
PACKET_F_MAX_VELOCITY = construct.Struct("PACKET_F_MAX_VELOCITY",
    construct.UBInt16("velocity"),                      # + 0x00
    )

F_PLAYER_EXPERIENCE = 0x39
SIZE_PACKET_F_PLAYER_EXPERIENCE = 0x0D
PACKET_F_PLAYER_EXPERIENCE = construct.Struct("PACKET_F_PLAYER_EXPERIENCE",
    construct.UBInt32("current_xp"),            # + 0x00
    construct.UBInt32("next_lvl_xp"),           # + 0x04
    construct.UBInt32("rested_xp"),             # + 0x08
    construct.UBInt8("level"),                  # + 0x0C
    )

F_PLAYER_RENOWN = 0x4E
SIZE_PACKET_F_PLAYER_RENOWN = 0x09
PACKET_F_PLAYER_RENOWN = construct.Struct("PACKET_F_PLAYER_RENOWN",
    construct.UBInt32("current_xp"),            # + 0x00
    construct.UBInt32("next_lvl_xp"),           # + 0x04
    construct.UBInt8("rank"),                   # + 0x08
    )

F_PLAYER_WEALTH = 0x52
SIZE_PACKET_F_PLAYER_WEALTH = 0x08
PACKET_F_PLAYER_WEALTH = construct.Struct("PACKET_F_PLAYER_WEALTH",
    construct.UBInt32("unk_dword_00"),                # + 0x00
    construct.UBInt32("player_money"),                # + 0x04
    )

F_REQUEST_CHAR_RESPONSE = 0x55
SIZE_PACKET_F_REQUEST_CHAR_RESPONSE = 0x20
PACKET_F_REQUEST_CHAR_RESPONSE = construct.Struct("PACKET_F_REQUEST_CHAR_RESPONSE",
    construct.Array(0x14, construct.UBInt8("unk_data_00")),     # + 0x00
    construct.UBInt32("remaining_lockout_time"),                # + 0x14
    construct.UBInt8("unk_byte_00"),                            # + 0x18
    construct.UBInt8("unk_byte_01"),                            # + 0x19
    construct.UBInt8("max_characters"),                         # + 0x1A
    construct.UBInt8("gameplay_rule_set_type"),                 # + 0x1B
    construct.UBInt8("last_switched_to_realm"),                 # + 0x1C
    construct.UBInt8("num_paid_name_changes_available"),        # + 0x1D
    construct.UBInt16("unk_word_00"),                           # + 0x1E
    )

S_PID_ASSIGN = 0x80
SIZE_PACKET_S_PID_ASSIGN = 0x30
PACKET_S_PID_ASSIGN = construct.Struct("PACKET_S_PID_ASSIGN",
    construct.UBInt16("session_id"),                            # + 0x00
    )

S_PONG = 0x81
SIZE_PACKET_S_PONG = 0x30
PACKET_S_PONG = construct.Struct("PACKET_S_PONG",
    construct.UBInt32("client_timestamp"),                     # + 0x00
    construct.UBInt64("timestamp"),                            # + 0x04
    construct.UBInt32("sequence"),                             # + 0x0C
    construct.UBInt32("unk_dword_00"),                         # + 0x10
    )

S_CONNECTED = 0x82
PACKET_S_CONNECTED = construct.Struct("PACKET_S_CONNECTED",
    construct.UBInt8("unk_byte_00"),                            # + 0x00
    construct.UBInt8("unk_byte_01"),                            # + 0x01
    construct.UBInt8("unk_byte_02"),                            # + 0x02
    construct.UBInt8("unk_byte_03"),                            # + 0x03
    construct.UBInt32("protocol_version"),                      # + 0x04
    construct.UBInt8("server_id"),                              # + 0x08
    construct.UBInt8("unk_byte_04"),                            # + 0x09
    construct.UBInt8("unk_byte_05"),                            # + 0x0A
    construct.UBInt8("unk_byte_06"),                            # + 0x0B
    construct.UBInt8("transfer_flag"),                          # + 0x0C
    construct.PascalString("username",
        length_field = construct.UBInt8("length")),             # + 0x..
    construct.PascalString("server_name",
        length_field = construct.UBInt8("length")),             # + 0x..
    construct.UBInt8("unk_byte_07"),                            # + 0x..
                        )

S_PLAYER_INITTED = 0x88
SIZE_PACKET_S_PLAYER_INITTED = 0x28 # TODO
PACKET_S_PLAYER_INITTED = construct.Struct("PACKET_S_PLAYER_INITTED",
    construct.UBInt16("object_id"),        # + 0x00
    construct.Padding(2),                  # + 0x02
    construct.UBInt32("character_id"),     # + 0x04
    construct.UBInt16("coord_z"),          # + 0x08
    construct.Padding(2),                  # + 0x0A
    construct.UBInt32("coord_x"),          # + 0x0C
    construct.UBInt32("coord_y"),          # + 0x10
    construct.UBInt16("coord_o"),          # + 0x14
    construct.Padding(1),                  # + 0x16
    construct.UBInt8("player_realm"),      # + 0x17
    construct.UBInt16("unk_word_00"),      # + 0x18
    construct.UBInt16("unk_word_01"),      # + 0x1A
    construct.UBInt16("region_id"),        # + 0x1C
    construct.UBInt16("instance_id"),      # + 0x1E
    construct.UBInt16("unk_word_02"),      # + 0x20
    construct.UBInt16("unk_word_03"),      # + 0x22
    construct.UBInt16("unk_word_04"),      # + 0x24
    construct.UBInt16("unk_word_05"),      # + 0x26
    )

F_RECEIVE_ENCRYPTKEY = 0x8A
SIZE_PACKET_F_RECEIVE_ENCRYPTKEY = 0x01
PACKET_F_RECEIVE_ENCRYPTKEY = construct.Struct("PACKET_F_RECEIVE_ENCRYPTKEY",
    construct.UBInt8("send_key"),                               # + 0x00
                        )

F_BAG_INFO = 0x95
SIZE_PACKET_F_BAG_INFO_COMMAND_0F = 0x10
PACKET_F_BAG_INFO_COMMAND_0F = construct.Struct("PACKET_F_BAG_INFO_COMMAND_0F",
    construct.ULInt16("num_backpack_slots"),                # + 0x00 , GameData.Player.numBackpackSlots
    construct.ULInt16("backpack_expansion_slots"),          # + 0x02 , GameData.Player.backpackExpansionSlots
    construct.ULInt32("backpack_expansion_slots_cost"),     # + 0x04 , GameData.Player.backpackExpansionSlotsCost
    construct.ULInt16("num_bank_slots"),                    # + 0x08 , GameData.Player.numBankSlots
    construct.ULInt16("bank_expansion_slots"),              # + 0x0A , GameData.Player.bankExpansionSlots
    construct.ULInt32("bank_expansion_slots_cost"),         # + 0x0C , GameData.Player.bankExpansionSlotsCost
    )

F_CHARACTER_INFO = 0xBE
SIZE_PACKET_F_CHARACTER_INFO = 0x00 # TODO
PACKET_F_CHARACTER_INFO = construct.Struct("PACKET_F_CHARACTER_INFO",
    # TODO
    )    
    
PACKET_F_CHARACTER_INFO_ABILITIES = construct.Struct("PACKET_F_CHARACTER_INFO_ABILITIES",
    construct.UBInt8("nb_abilities"),      # + 0x00
    construct.Padding(2),                  # + 0x01
    construct.Array(lambda ctx: ctx.nb_abilities, ABILITY_STRUCT)
    )    
    
F_PLAYER_INIT_COMPLETE = 0xEF
SIZE_PACKET_F_PLAYER_INIT_COMPLETE = 0x02
PACKET_F_PLAYER_INIT_COMPLETE = construct.Struct("PACKET_F_PLAYER_INIT_COMPLETE",
    construct.UBInt16("unk_word_00"),     # + 0x00
    )

F_PLAYER_RANK_UPDATE = 0xF4
SIZE_PACKET_F_PLAYER_RANK_UPDATE = 0x04
PACKET_F_PLAYER_RANK_UPDATE = construct.Struct("PACKET_F_PLAYER_RANK_UPDATE",
    construct.UBInt8("unk_byte_00"),      # + 0x00
    construct.UBInt8("unk_byte_01"),      # + 0x01
    construct.UBInt16("object_id"),       # + 0x02
    )
    
F_TRADE_SKILL_UPDATE = 0xF9
SIZE_PACKET_F_TRADE_SKILL_UPDATE = 0x04
PACKET_F_TRADE_SKILL_UPDATE = construct.Struct("PACKET_F_TRADE_SKILL_UPDATE",
    construct.UBInt8("tradeskill_id"),    # + 0x00
    construct.Padding(1),                 # + 0x01
    construct.UBInt16("level"),           # + 0x02
    )
    
##########################################################################

F_QUEST = 0x02
SIZE_PACKET_F_QUEST = 0x00 # TODO
PACKET_F_QUEST = construct.Struct("PACKET_F_QUEST",
    # TODO
    )

F_UPDATE_SIEGE_LOOK_AT = 0x03
SIZE_PACKET_F_UPDATE_SIEGE_LOOK_AT = 0x00 # TODO
PACKET_F_UPDATE_SIEGE_LOOK_AT = construct.Struct("PACKET_F_UPDATE_SIEGE_LOOK_AT",
    # TODO
    )

F_TEXT = 0x07
SIZE_PACKET_F_TEXT = 0x00 # TODO
PACKET_F_TEXT = construct.Struct("PACKET_F_TEXT",
    # TODO
    )

F_OBJECT_STATE = 0x09
SIZE_PACKET_F_OBJECT_STATE = 0x00 # TODO
PACKET_F_OBJECT_STATE = construct.Struct("PACKET_F_OBJECT_STATE",
    # TODO
    )

F_OBJECT_DEATH = 0x0A
SIZE_PACKET_F_OBJECT_DEATH = 0x00 # TODO
PACKET_F_OBJECT_DEATH = construct.Struct("PACKET_F_OBJECT_DEATH",
    # TODO
    )

F_PLAYER_QUIT = 0x0C
SIZE_PACKET_F_PLAYER_QUIT = 0x00 # TODO
PACKET_F_PLAYER_QUIT = construct.Struct("PACKET_F_PLAYER_QUIT",
    # TODO
    )

F_DUMP_STATICS = 0x0D
SIZE_PACKET_F_DUMP_STATICS = 0x00 # TODO
PACKET_F_DUMP_STATICS = construct.Struct("PACKET_F_DUMP_STATICS",
    # TODO
    )

F_DISCONNECT = 0x10
SIZE_PACKET_F_DISCONNECT = 0x00 # TODO
PACKET_F_DISCONNECT = construct.Struct("PACKET_F_DISCONNECT",
    # TODO
    )

F_HEARTBEAT = 0x11
SIZE_PACKET_F_HEARTBEAT = 0x00 # TODO
PACKET_F_HEARTBEAT = construct.Struct("PACKET_F_HEARTBEAT",
    # TODO
    )

F_REQUEST_CHAR_TEMPLATES = 0x13
SIZE_PACKET_F_REQUEST_CHAR_TEMPLATES = 0x00 # TODO
PACKET_F_REQUEST_CHAR_TEMPLATES = construct.Struct("PACKET_F_REQUEST_CHAR_TEMPLATES",
    # TODO
    )

F_HIT_PLAYER = 0x14
SIZE_PACKET_F_HIT_PLAYER = 0x00 # TODO
PACKET_F_HIT_PLAYER = construct.Struct("PACKET_F_HIT_PLAYER",
    # TODO
    )

F_DEATHSPAM = 0x15
SIZE_PACKET_F_DEATHSPAM = 0x00 # TODO
PACKET_F_DEATHSPAM = construct.Struct("PACKET_F_DEATHSPAM",
    # TODO
    )

F_REQUEST_INIT_OBJECT = 0x16
SIZE_PACKET_F_REQUEST_INIT_OBJECT = 0x00 # TODO
PACKET_F_REQUEST_INIT_OBJECT = construct.Struct("PACKET_F_REQUEST_INIT_OBJECT",
    # TODO
    )

F_PLAYER_INFO = 0x18
SIZE_PACKET_F_PLAYER_INFO = 0x00 # TODO
PACKET_F_PLAYER_INFO = construct.Struct("PACKET_F_PLAYER_INFO",
    # TODO
    )

F_WORLD_ENTER = 0x19
SIZE_PACKET_F_WORLD_ENTER = 0x00 # TODO
PACKET_F_WORLD_ENTER = construct.Struct("PACKET_F_WORLD_ENTER",
    # TODO
    )

F_CAMPAIGN_STATUS = 0x1A
SIZE_PACKET_F_CAMPAIGN_STATUS = 0x00 # TODO
PACKET_F_CAMPAIGN_STATUS = construct.Struct("PACKET_F_CAMPAIGN_STATUS",
    # TODO
    )

F_REQ_CAMPAIGN_STATUS = 0x1B
SIZE_PACKET_F_REQ_CAMPAIGN_STATUS = 0x00 # TODO
PACKET_F_REQ_CAMPAIGN_STATUS = construct.Struct("PACKET_F_REQ_CAMPAIGN_STATUS",
    # TODO
    )

F_GUILD_DATA = 0x1D
SIZE_PACKET_F_GUILD_DATA = 0x00 # TODO
PACKET_F_GUILD_DATA = construct.Struct("PACKET_F_GUILD_DATA",
    # TODO
    )

F_SWITCH_REGION = 0x1F
SIZE_PACKET_F_SWITCH_REGION = 0x00 # TODO
PACKET_F_SWITCH_REGION = construct.Struct("PACKET_F_SWITCH_REGION",
    # TODO
    )

F_PET_INFO = 0x20
SIZE_PACKET_F_PET_INFO = 0x00 # TODO
PACKET_F_PET_INFO = construct.Struct("PACKET_F_PET_INFO",
    # TODO
    )

F_PLAYER_CLEAR_DEATH = 0x21
SIZE_PACKET_F_PLAYER_CLEAR_DEATH = 0x00 # TODO
PACKET_F_PLAYER_CLEAR_DEATH = construct.Struct("PACKET_F_PLAYER_CLEAR_DEATH",
    # TODO
    )

F_COMMAND_CONTROLLED = 0x22
SIZE_PACKET_F_COMMAND_CONTROLLED = 0x00 # TODO
PACKET_F_COMMAND_CONTROLLED = construct.Struct("PACKET_F_COMMAND_CONTROLLED",
    # TODO
    )

F_GUILD_COMMAND = 0x25
SIZE_PACKET_F_GUILD_COMMAND = 0x00 # TODO
PACKET_F_GUILD_COMMAND = construct.Struct("PACKET_F_GUILD_COMMAND",
    # TODO
    )

F_REQUEST_TOK_REWARD = 0x27
SIZE_PACKET_F_REQUEST_TOK_REWARD = 0x00 # TODO
PACKET_F_REQUEST_TOK_REWARD = construct.Struct("PACKET_F_REQUEST_TOK_REWARD",
    # TODO
    )

F_SURVEY_BEGIN = 0x28
SIZE_PACKET_F_SURVEY_BEGIN = 0x00 # TODO
PACKET_F_SURVEY_BEGIN = construct.Struct("PACKET_F_SURVEY_BEGIN",
    # TODO
    )

F_SHOW_DIALOG = 0x29
SIZE_PACKET_F_SHOW_DIALOG = 0x00 # TODO
PACKET_F_SHOW_DIALOG = construct.Struct("PACKET_F_SHOW_DIALOG",
    # TODO
    )

F_PLAYERORG_APPROVAL = 0x2A
SIZE_PACKET_F_PLAYERORG_APPROVAL = 0x00 # TODO
PACKET_F_PLAYERORG_APPROVAL = construct.Struct("PACKET_F_PLAYERORG_APPROVAL",
    # TODO
    )

F_QUEST_INFO = 0x2B
SIZE_PACKET_F_QUEST_INFO = 0x00 # TODO
PACKET_F_QUEST_INFO = construct.Struct("PACKET_F_QUEST_INFO",
    # TODO
    )

F_INVITE_GROUP = 0x2F
SIZE_PACKET_F_INVITE_GROUP = 0x00 # TODO
PACKET_F_INVITE_GROUP = construct.Struct("PACKET_F_INVITE_GROUP",
    # TODO
    )

F_JOIN_GROUP = 0x30
SIZE_PACKET_F_JOIN_GROUP = 0x00 # TODO
PACKET_F_JOIN_GROUP = construct.Struct("PACKET_F_JOIN_GROUP",
    # TODO
    )

F_PLAYER_DEATH = 0x31
SIZE_PACKET_F_PLAYER_DEATH = 0x00 # TODO
PACKET_F_PLAYER_DEATH = construct.Struct("PACKET_F_PLAYER_DEATH",
    # TODO
    )

F_GROUP_COMMAND = 0x37
SIZE_PACKET_F_GROUP_COMMAND = 0x00 # TODO
PACKET_F_GROUP_COMMAND = construct.Struct("PACKET_F_GROUP_COMMAND",
    # TODO
    )

F_ZONEJUMP = 0x38
SIZE_PACKET_F_ZONEJUMP = 0x00 # TODO
PACKET_F_ZONEJUMP = construct.Struct("PACKET_F_ZONEJUMP",
    # TODO
    )

F_XENON_VOICE = 0x3A
SIZE_PACKET_F_XENON_VOICE = 0x00 # TODO
PACKET_F_XENON_VOICE = construct.Struct("PACKET_F_XENON_VOICE",
    # TODO
    )

F_REQUEST_WORLD_LARGE = 0x40
SIZE_PACKET_F_REQUEST_WORLD_LARGE = 0x00 # TODO
PACKET_F_REQUEST_WORLD_LARGE = construct.Struct("PACKET_F_REQUEST_WORLD_LARGE",
    # TODO
    )

F_ACTION_COUNTER_INFO = 0x41
SIZE_PACKET_F_ACTION_COUNTER_INFO = 0x00 # TODO
PACKET_F_ACTION_COUNTER_INFO = construct.Struct("PACKET_F_ACTION_COUNTER_INFO",
    # TODO
    )

F_ACTION_COUNTER_UPDATE = 0x44
SIZE_PACKET_F_ACTION_COUNTER_UPDATE = 0x00 # TODO
PACKET_F_ACTION_COUNTER_UPDATE = construct.Struct("PACKET_F_ACTION_COUNTER_UPDATE",
    # TODO
    )

F_PLAYER_STATS = 0x46
SIZE_PACKET_F_PLAYER_STATS = 0x00 # TODO
PACKET_F_PLAYER_STATS = construct.Struct("PACKET_F_PLAYER_STATS",
    # TODO
    )

F_MONSTER_STATS = 0x47
SIZE_PACKET_F_MONSTER_STATS = 0x00 # TODO
PACKET_F_MONSTER_STATS = construct.Struct("PACKET_F_MONSTER_STATS",
    # TODO
    )

F_PLAY_EFFECT = 0x48
SIZE_PACKET_F_PLAY_EFFECT = 0x00 # TODO
PACKET_F_PLAY_EFFECT = construct.Struct("PACKET_F_PLAY_EFFECT",
    # TODO
    )

F_REMOVE_PLAYER = 0x49
SIZE_PACKET_F_REMOVE_PLAYER = 0x00 # TODO
PACKET_F_REMOVE_PLAYER = construct.Struct("PACKET_F_REMOVE_PLAYER",
    # TODO
    )

F_ZONEJUMP_FAILED = 0x4A
SIZE_PACKET_F_ZONEJUMP_FAILED = 0x00 # TODO
PACKET_F_ZONEJUMP_FAILED = construct.Struct("PACKET_F_ZONEJUMP_FAILED",
    # TODO
    )

F_TRADE_STATUS = 0x4B
SIZE_PACKET_F_TRADE_STATUS = 0x00 # TODO
PACKET_F_TRADE_STATUS = construct.Struct("PACKET_F_TRADE_STATUS",
    # TODO
    )

F_MOUNT_UPDATE = 0x4F
SIZE_PACKET_F_MOUNT_UPDATE = 0x00 # TODO
PACKET_F_MOUNT_UPDATE = construct.Struct("PACKET_F_MOUNT_UPDATE",
    # TODO
    )

F_PLAYER_LEVEL_UP = 0x50
SIZE_PACKET_F_PLAYER_LEVEL_UP = 0x00 # TODO
PACKET_F_PLAYER_LEVEL_UP = construct.Struct("PACKET_F_PLAYER_LEVEL_UP",
    # TODO
    )

F_ANIMATION = 0x51
SIZE_PACKET_F_ANIMATION = 0x00 # TODO
PACKET_F_ANIMATION = construct.Struct("PACKET_F_ANIMATION",
    # TODO
    )

F_TROPHY_SETLOCATION = 0x53
SIZE_PACKET_F_TROPHY_SETLOCATION = 0x00 # TODO
PACKET_F_TROPHY_SETLOCATION = construct.Struct("PACKET_F_TROPHY_SETLOCATION",
    # TODO
    )

F_REQUEST_CHAR_ERROR = 0x56
SIZE_PACKET_F_REQUEST_CHAR_ERROR = 0x00 # TODO
PACKET_F_REQUEST_CHAR_ERROR = construct.Struct("PACKET_F_REQUEST_CHAR_ERROR",
    # TODO
    )

F_CHARACTER_PREFS = 0x57
SIZE_PACKET_F_CHARACTER_PREFS = 0x00 # TODO
PACKET_F_CHARACTER_PREFS = construct.Struct("PACKET_F_CHARACTER_PREFS",
    # TODO
    )

F_SEND_CHARACTER_RESPONSE = 0x58
SIZE_PACKET_F_SEND_CHARACTER_RESPONSE = 0x00 # TODO
PACKET_F_SEND_CHARACTER_RESPONSE = construct.Struct("PACKET_F_SEND_CHARACTER_RESPONSE",
    # TODO
    )

F_SEND_CHARACTER_ERROR = 0x59
SIZE_PACKET_F_SEND_CHARACTER_ERROR = 0x00 # TODO
PACKET_F_SEND_CHARACTER_ERROR = construct.Struct("PACKET_F_SEND_CHARACTER_ERROR",
    # TODO
    )

F_PING_DATAGRAM = 0x5A
SIZE_PACKET_F_PING_DATAGRAM = 0x00 # TODO
PACKET_F_PING_DATAGRAM = construct.Struct("PACKET_F_PING_DATAGRAM",
    # TODO
    )

F_PQLOOT_TRIGGER = 0x5D
SIZE_PACKET_F_PQLOOT_TRIGGER = 0x00 # TODO
PACKET_F_PQLOOT_TRIGGER = construct.Struct("PACKET_F_PQLOOT_TRIGGER",
    # TODO
    )

F_SET_TARGET = 0x5E
SIZE_PACKET_F_SET_TARGET = 0x00 # TODO
PACKET_F_SET_TARGET = construct.Struct("PACKET_F_SET_TARGET",
    # TODO
    )

F_MYSTERY_BAG = 0x60
SIZE_PACKET_F_MYSTERY_BAG = 0x00 # TODO
PACKET_F_MYSTERY_BAG = construct.Struct("PACKET_F_MYSTERY_BAG",
    # TODO
    )

F_PLAY_SOUND = 0x61
SIZE_PACKET_F_PLAY_SOUND = 0x00 # TODO
PACKET_F_PLAY_SOUND = construct.Struct("PACKET_F_PLAY_SOUND",
    # TODO
    )

F_PLAYER_STATE2 = 0x62
SIZE_PACKET_F_PLAYER_STATE2 = 0x00 # TODO
PACKET_F_PLAYER_STATE2 = construct.Struct("PACKET_F_PLAYER_STATE2",
    # TODO
    )

F_QUERY_NAME = 0x63
SIZE_PACKET_F_QUERY_NAME = 0x00 # TODO
PACKET_F_QUERY_NAME = construct.Struct("PACKET_F_QUERY_NAME",
    # TODO
    )

F_QUERY_NAME_RESPONSE = 0x64
SIZE_PACKET_F_QUERY_NAME_RESPONSE = 0x00 # TODO
PACKET_F_QUERY_NAME_RESPONSE = construct.Struct("PACKET_F_QUERY_NAME_RESPONSE",
    # TODO
    )

F_ADD_NAME = 0x65
SIZE_PACKET_F_ADD_NAME = 0x00 # TODO
PACKET_F_ADD_NAME = construct.Struct("PACKET_F_ADD_NAME",
    # TODO
    )

F_DELETE_NAME = 0x68
SIZE_PACKET_F_DELETE_NAME = 0x00 # TODO
PACKET_F_DELETE_NAME = construct.Struct("PACKET_F_DELETE_NAME",
    # TODO
    )

F_CHECK_NAME = 0x6A
SIZE_PACKET_F_CHECK_NAME = 0x00 # TODO
PACKET_F_CHECK_NAME = construct.Struct("PACKET_F_CHECK_NAME",
    # TODO
    )

F_CHECK_NAME_RESPONSE = 0x6B
SIZE_PACKET_F_CHECK_NAME_RESPONSE = 0x00 # TODO
PACKET_F_CHECK_NAME_RESPONSE = construct.Struct("PACKET_F_CHECK_NAME_RESPONSE",
    # TODO
    )

F_LOCALIZED_STRING = 0x6F
SIZE_PACKET_F_LOCALIZED_STRING = 0x00 # TODO
PACKET_F_LOCALIZED_STRING = construct.Struct("PACKET_F_LOCALIZED_STRING",
    # TODO
    )

F_KILLING_SPREE = 0x70
SIZE_PACKET_F_KILLING_SPREE = 0x00 # TODO
PACKET_F_KILLING_SPREE = construct.Struct("PACKET_F_KILLING_SPREE",
    # TODO
    )

F_CREATE_STATIC = 0x71
SIZE_PACKET_F_CREATE_STATIC = 0x00 # TODO
PACKET_F_CREATE_STATIC = construct.Struct("PACKET_F_CREATE_STATIC",
    # TODO
    )

F_CREATE_MONSTER = 0x72
SIZE_PACKET_F_CREATE_MONSTER = 0x00 # TODO
PACKET_F_CREATE_MONSTER = construct.Struct("PACKET_F_CREATE_MONSTER",
    # TODO
    )

F_PLAYER_IMAGENUM = 0x73
SIZE_PACKET_F_PLAYER_IMAGENUM = 0x00 # TODO
PACKET_F_PLAYER_IMAGENUM = construct.Struct("PACKET_F_PLAYER_IMAGENUM",
    # TODO
    )

F_TRANSFER_ITEM = 0x75
SIZE_PACKET_F_TRANSFER_ITEM = 0x00 # TODO
PACKET_F_TRANSFER_ITEM = construct.Struct("PACKET_F_TRANSFER_ITEM",
    # TODO
    )

F_CRAFTING_STATUS = 0x79
SIZE_PACKET_F_CRAFTING_STATUS = 0x00 # TODO
PACKET_F_CRAFTING_STATUS = construct.Struct("PACKET_F_CRAFTING_STATUS",
    # TODO
    )

F_REQUEST_LASTNAME = 0x7A
SIZE_PACKET_F_REQUEST_LASTNAME = 0x00 # TODO
PACKET_F_REQUEST_LASTNAME = construct.Struct("PACKET_F_REQUEST_LASTNAME",
    # TODO
    )

F_REQUEST_INIT_PLAYER = 0x7D
SIZE_PACKET_F_REQUEST_INIT_PLAYER = 0x00 # TODO
PACKET_F_REQUEST_INIT_PLAYER = construct.Struct("PACKET_F_REQUEST_INIT_PLAYER",
    # TODO
    )

F_SET_ABILITY_TIMER = 0x7E
SIZE_PACKET_F_SET_ABILITY_TIMER = 0x00 # TODO
PACKET_F_SET_ABILITY_TIMER = construct.Struct("PACKET_F_SET_ABILITY_TIMER",
    # TODO
    )

S_WORLD_SENT = 0x83
SIZE_PACKET_S_WORLD_SENT = 0x00 # TODO
PACKET_S_WORLD_SENT = construct.Struct("PACKET_S_WORLD_SENT",
    # TODO
    )

S_NOT_CONNECTED = 0x84
SIZE_PACKET_S_NOT_CONNECTED = 0x00 # TODO
PACKET_S_NOT_CONNECTED = construct.Struct("PACKET_S_NOT_CONNECTED",
    # TODO
    )

S_GAME_OPENED = 0x85
SIZE_PACKET_S_GAME_OPENED = 0x00 # TODO
PACKET_S_GAME_OPENED = construct.Struct("PACKET_S_GAME_OPENED",
    # TODO
    )

F_MAIL = 0x86
SIZE_PACKET_F_MAIL = 0x00 # TODO
PACKET_F_MAIL = construct.Struct("PACKET_F_MAIL",
    # TODO
    )

S_DATAGRAM_ESTABLISHED = 0x87
SIZE_PACKET_S_DATAGRAM_ESTABLISHED = 0x00 # TODO
PACKET_S_DATAGRAM_ESTABLISHED = construct.Struct("PACKET_S_DATAGRAM_ESTABLISHED",
    # TODO
    )

S_PLAYER_LOADED = 0x89
SIZE_PACKET_S_PLAYER_LOADED = 0x00 # TODO
PACKET_S_PLAYER_LOADED = construct.Struct("PACKET_S_PLAYER_LOADED",
    # TODO
    )

F_MORALE_LIST = 0x8C
SIZE_PACKET_F_MORALE_LIST = 0x00 # TODO
PACKET_F_MORALE_LIST = construct.Struct("PACKET_F_MORALE_LIST",
    # TODO
    )

F_SURVEY_ADDQUESTION = 0x8D
SIZE_PACKET_F_SURVEY_ADDQUESTION = 0x00 # TODO
PACKET_F_SURVEY_ADDQUESTION = construct.Struct("PACKET_F_SURVEY_ADDQUESTION",
    # TODO
    )

F_SURVEY_END = 0x8E
SIZE_PACKET_F_SURVEY_END = 0x00 # TODO
PACKET_F_SURVEY_END = construct.Struct("PACKET_F_SURVEY_END",
    # TODO
    )

F_SURVEY_RESULT = 0x8F
SIZE_PACKET_F_SURVEY_RESULT = 0x00 # TODO
PACKET_F_SURVEY_RESULT = construct.Struct("PACKET_F_SURVEY_RESULT",
    # TODO
    )

F_EMOTE = 0x90
SIZE_PACKET_F_EMOTE = 0x00 # TODO
PACKET_F_EMOTE = construct.Struct("PACKET_F_EMOTE",
    # TODO
    )

F_CREATE_CHARACTER = 0x91
SIZE_PACKET_F_CREATE_CHARACTER = 0x00 # TODO
PACKET_F_CREATE_CHARACTER = construct.Struct("PACKET_F_CREATE_CHARACTER",
    # TODO
    )

F_DELETE_CHARACTER = 0x92
SIZE_PACKET_F_DELETE_CHARACTER = 0x00 # TODO
PACKET_F_DELETE_CHARACTER = construct.Struct("PACKET_F_DELETE_CHARACTER",
    # TODO
    )

F_GFX_MOD = 0x93
SIZE_PACKET_F_GFX_MOD = 0x00 # TODO
PACKET_F_GFX_MOD = construct.Struct("PACKET_F_GFX_MOD",
    # TODO
    )

F_INSTANCE_INFO = 0x94
SIZE_PACKET_F_INSTANCE_INFO = 0x00 # TODO
PACKET_F_INSTANCE_INFO = construct.Struct("PACKET_F_INSTANCE_INFO",
    # TODO
    )

F_KEEP_STATUS = 0x96
SIZE_PACKET_F_KEEP_STATUS = 0x00 # TODO
PACKET_F_KEEP_STATUS = construct.Struct("PACKET_F_KEEP_STATUS",
    # TODO
    )

F_PLAY_TIME_STATS = 0x97
SIZE_PACKET_F_PLAY_TIME_STATS = 0x00 # TODO
PACKET_F_PLAY_TIME_STATS = construct.Struct("PACKET_F_PLAY_TIME_STATS",
    # TODO
    )

F_CATAPULT = 0x98
SIZE_PACKET_F_CATAPULT = 0x00 # TODO
PACKET_F_CATAPULT = construct.Struct("PACKET_F_CATAPULT",
    # TODO
    )

F_GRAVITY_UPDATE = 0x99
SIZE_PACKET_F_GRAVITY_UPDATE = 0x00 # TODO
PACKET_F_GRAVITY_UPDATE = construct.Struct("PACKET_F_GRAVITY_UPDATE",
    # TODO
    )

F_UPDATE_LASTNAME = 0x9B
SIZE_PACKET_F_UPDATE_LASTNAME = 0x00 # TODO
PACKET_F_UPDATE_LASTNAME = construct.Struct("PACKET_F_UPDATE_LASTNAME",
    # TODO
    )

F_GET_CULTIVATION_INFO = 0x9E
SIZE_PACKET_F_GET_CULTIVATION_INFO = 0x00 # TODO
PACKET_F_GET_CULTIVATION_INFO = construct.Struct("PACKET_F_GET_CULTIVATION_INFO",
    # TODO
    )

F_CRASH_PACKET = 0x9F
SIZE_PACKET_F_CRASH_PACKET = 0x00 # TODO
PACKET_F_CRASH_PACKET = construct.Struct("PACKET_F_CRASH_PACKET",
    # TODO
    )

F_LOGINQUEUE = 0xA0
SIZE_PACKET_F_LOGINQUEUE = 0x00 # TODO
PACKET_F_LOGINQUEUE = construct.Struct("PACKET_F_LOGINQUEUE",
    # TODO
    )

F_INTERRUPT = 0xA1
SIZE_PACKET_F_INTERRUPT = 0x00 # TODO
PACKET_F_INTERRUPT = construct.Struct("PACKET_F_INTERRUPT",
    # TODO
    )

F_INSTANCE_SELECTED = 0xA2
SIZE_PACKET_F_INSTANCE_SELECTED = 0x00 # TODO
PACKET_F_INSTANCE_SELECTED = construct.Struct("PACKET_F_INSTANCE_SELECTED",
    # TODO
    )

F_ACTIVE_EFFECTS = 0xA3
SIZE_PACKET_F_ACTIVE_EFFECTS = 0x00 # TODO
PACKET_F_ACTIVE_EFFECTS = construct.Struct("PACKET_F_ACTIVE_EFFECTS",
    # TODO
    )

F_START_SIEGE_MULTIUSER = 0xA6
SIZE_PACKET_F_START_SIEGE_MULTIUSER = 0x00 # TODO
PACKET_F_START_SIEGE_MULTIUSER = construct.Struct("PACKET_F_START_SIEGE_MULTIUSER",
    # TODO
    )

F_SIEGE_WEAPON_RESULTS = 0xA7
SIZE_PACKET_F_SIEGE_WEAPON_RESULTS = 0x00 # TODO
PACKET_F_SIEGE_WEAPON_RESULTS = construct.Struct("PACKET_F_SIEGE_WEAPON_RESULTS",
    # TODO
    )

F_INTERACT_QUEUE = 0xA8
SIZE_PACKET_F_INTERACT_QUEUE = 0x00 # TODO
PACKET_F_INTERACT_QUEUE = construct.Struct("PACKET_F_INTERACT_QUEUE",
    # TODO
    )

F_UPDATE_HOT_SPOT = 0xA9
SIZE_PACKET_F_UPDATE_HOT_SPOT = 0x00 # TODO
PACKET_F_UPDATE_HOT_SPOT = construct.Struct("PACKET_F_UPDATE_HOT_SPOT",
    # TODO
    )

F_GET_ITEM = 0xAA
SIZE_PACKET_F_GET_ITEM = 0x00 # TODO
PACKET_F_GET_ITEM = construct.Struct("PACKET_F_GET_ITEM",
    # TODO
    )

F_DUEL = 0xAB
SIZE_PACKET_F_DUEL = 0x00 # TODO
PACKET_F_DUEL = construct.Struct("PACKET_F_DUEL",
    # TODO
    )

F_PLAYER_JUMP = 0xAC
SIZE_PACKET_F_PLAYER_JUMP = 0x00 # TODO
PACKET_F_PLAYER_JUMP = construct.Struct("PACKET_F_PLAYER_JUMP",
    # TODO
    )

F_INTRO_CINEMA = 0xAD
SIZE_PACKET_F_INTRO_CINEMA = 0x00 # TODO
PACKET_F_INTRO_CINEMA = construct.Struct("PACKET_F_INTRO_CINEMA",
    # TODO
    )

F_MAGUS_DISC_UPDATE = 0xAE
SIZE_PACKET_F_MAGUS_DISC_UPDATE = 0x00 # TODO
PACKET_F_MAGUS_DISC_UPDATE = construct.Struct("PACKET_F_MAGUS_DISC_UPDATE",
    # TODO
    )

F_FIRE_SIEGE_WEAPON = 0xAF
SIZE_PACKET_F_FIRE_SIEGE_WEAPON = 0x00 # TODO
PACKET_F_FIRE_SIEGE_WEAPON = construct.Struct("PACKET_F_FIRE_SIEGE_WEAPON",
    # TODO
    )

F_GRAPHICAL_REVISION = 0xB0
SIZE_PACKET_F_GRAPHICAL_REVISION = 0x00 # TODO
PACKET_F_GRAPHICAL_REVISION = construct.Struct("PACKET_F_GRAPHICAL_REVISION",
    # TODO
    )

F_AUCTION_POST_ITEM = 0xB2
SIZE_PACKET_F_AUCTION_POST_ITEM = 0x00 # TODO
PACKET_F_AUCTION_POST_ITEM = construct.Struct("PACKET_F_AUCTION_POST_ITEM",
    # TODO
    )

F_CAST_PLAYER_EFFECT = 0xB3
SIZE_PACKET_F_CAST_PLAYER_EFFECT = 0x00 # TODO
PACKET_F_CAST_PLAYER_EFFECT = construct.Struct("PACKET_F_CAST_PLAYER_EFFECT",
    # TODO
    )

F_AUCTION_SEARCH_QUERY = 0xB4
SIZE_PACKET_F_AUCTION_SEARCH_QUERY = 0x00 # TODO
PACKET_F_AUCTION_SEARCH_QUERY = construct.Struct("PACKET_F_AUCTION_SEARCH_QUERY",
    # TODO
    )

F_FLIGHT = 0xB5
SIZE_PACKET_F_FLIGHT = 0x00 # TODO
PACKET_F_FLIGHT = construct.Struct("PACKET_F_FLIGHT",
    # TODO
    )

F_SOCIAL_NETWORK = 0xB6
SIZE_PACKET_F_SOCIAL_NETWORK = 0x00 # TODO
PACKET_F_SOCIAL_NETWORK = construct.Struct("PACKET_F_SOCIAL_NETWORK",
    # TODO
    )

F_AUCTION_SEARCH_RESULT = 0xB7
SIZE_PACKET_F_AUCTION_SEARCH_RESULT = 0x00 # TODO
PACKET_F_AUCTION_SEARCH_RESULT = construct.Struct("PACKET_F_AUCTION_SEARCH_RESULT",
    # TODO
    )

F_AUCTION_BID_ITEM = 0xBB
SIZE_PACKET_F_AUCTION_BID_ITEM = 0x00 # TODO
PACKET_F_AUCTION_BID_ITEM = construct.Struct("PACKET_F_AUCTION_BID_ITEM",
    # TODO
    )

F_ESTABLISH_DATAGRAM = 0xBC
SIZE_PACKET_F_ESTABLISH_DATAGRAM = 0x00 # TODO
PACKET_F_ESTABLISH_DATAGRAM = construct.Struct("PACKET_F_ESTABLISH_DATAGRAM",
    # TODO
    )

F_PLAYER_INVENTORY = 0xBD
SIZE_PACKET_F_PLAYER_INVENTORY = 0x00 # TODO
PACKET_F_PLAYER_INVENTORY = construct.Struct("PACKET_F_PLAYER_INVENTORY",
    # TODO
    )

F_INIT_STORE = 0xBF
SIZE_PACKET_F_INIT_STORE = 0x00 # TODO
PACKET_F_INIT_STORE = construct.Struct("PACKET_F_INIT_STORE",
    # TODO
    )

F_STORE_BUY_BACK = 0xC0
SIZE_PACKET_F_STORE_BUY_BACK = 0x00 # TODO
PACKET_F_STORE_BUY_BACK = construct.Struct("PACKET_F_STORE_BUY_BACK",
    # TODO
    )

F_OBJECTIVE_INFO = 0xC1
SIZE_PACKET_F_OBJECTIVE_INFO = 0x00 # TODO
PACKET_F_OBJECTIVE_INFO = construct.Struct("PACKET_F_OBJECTIVE_INFO",
    # TODO
    )

F_OBJECTIVE_UPDATE = 0xC2
SIZE_PACKET_F_OBJECTIVE_UPDATE = 0x00 # TODO
PACKET_F_OBJECTIVE_UPDATE = construct.Struct("PACKET_F_OBJECTIVE_UPDATE",
    # TODO
    )

F_SCENARIO_INFO = 0xC3
SIZE_PACKET_F_SCENARIO_INFO = 0x00 # TODO
PACKET_F_SCENARIO_INFO = construct.Struct("PACKET_F_SCENARIO_INFO",
    # TODO
    )

F_SCENARIO_POINT_UPDATE = 0xC4
SIZE_PACKET_F_SCENARIO_POINT_UPDATE = 0x00 # TODO
PACKET_F_SCENARIO_POINT_UPDATE = construct.Struct("PACKET_F_SCENARIO_POINT_UPDATE",
    # TODO
    )

F_OBJECTIVE_STATE = 0xC5
SIZE_PACKET_F_OBJECTIVE_STATE = 0x00 # TODO
PACKET_F_OBJECTIVE_STATE = construct.Struct("PACKET_F_OBJECTIVE_STATE",
    # TODO
    )

F_REALM_BONUS = 0xC6
SIZE_PACKET_F_REALM_BONUS = 0x00 # TODO
PACKET_F_REALM_BONUS = construct.Struct("PACKET_F_REALM_BONUS",
    # TODO
    )

F_OBJECTIVE_CONTROL = 0xC7
SIZE_PACKET_F_OBJECTIVE_CONTROL = 0x00 # TODO
PACKET_F_OBJECTIVE_CONTROL = construct.Struct("PACKET_F_OBJECTIVE_CONTROL",
    # TODO
    )

F_SCENARIO_PLAYER_INFO = 0xC9
SIZE_PACKET_F_SCENARIO_PLAYER_INFO = 0x00 # TODO
PACKET_F_SCENARIO_PLAYER_INFO = construct.Struct("PACKET_F_SCENARIO_PLAYER_INFO",
    # TODO
    )

F_FLAG_OBJECT_STATE = 0xCA
SIZE_PACKET_F_FLAG_OBJECT_STATE = 0x00 # TODO
PACKET_F_FLAG_OBJECT_STATE = construct.Struct("PACKET_F_FLAG_OBJECT_STATE",
    # TODO
    )

F_FLAG_OBJECT_LOCATION = 0xCB
SIZE_PACKET_F_FLAG_OBJECT_LOCATION = 0x00 # TODO
PACKET_F_FLAG_OBJECT_LOCATION = construct.Struct("PACKET_F_FLAG_OBJECT_LOCATION",
    # TODO
    )

F_CITY_CAPTURE = 0xCC
SIZE_PACKET_F_CITY_CAPTURE = 0x00 # TODO
PACKET_F_CITY_CAPTURE = construct.Struct("PACKET_F_CITY_CAPTURE",
    # TODO
    )

F_ZONE_CAPTURE = 0xCD
SIZE_PACKET_F_ZONE_CAPTURE = 0x00 # TODO
PACKET_F_ZONE_CAPTURE = construct.Struct("PACKET_F_ZONE_CAPTURE",
    # TODO
    )

F_SALVAGE_ITEM = 0xCE
SIZE_PACKET_F_SALVAGE_ITEM = 0x00 # TODO
PACKET_F_SALVAGE_ITEM = construct.Struct("PACKET_F_SALVAGE_ITEM",
    # TODO
    )

F_AUCTION_BID_STATUS = 0xCF
SIZE_PACKET_F_AUCTION_BID_STATUS = 0x00 # TODO
PACKET_F_AUCTION_BID_STATUS = construct.Struct("PACKET_F_AUCTION_BID_STATUS",
    # TODO
    )

F_PUNKBUSTER = 0xD0
SIZE_PACKET_F_PUNKBUSTER = 0x00 # TODO
PACKET_F_PUNKBUSTER = construct.Struct("PACKET_F_PUNKBUSTER",
    # TODO
    )

F_ITEM_SET_DATA = 0xD1
SIZE_PACKET_F_ITEM_SET_DATA = 0x00 # TODO
PACKET_F_ITEM_SET_DATA = construct.Struct("PACKET_F_ITEM_SET_DATA",
    # TODO
    )

F_INTERACT = 0xD2
SIZE_PACKET_F_INTERACT = 0x00 # TODO
PACKET_F_INTERACT = construct.Struct("PACKET_F_INTERACT",
    # TODO
    )

F_DO_ABILITY = 0xD5
SIZE_PACKET_F_DO_ABILITY = 0x00 # TODO
PACKET_F_DO_ABILITY = construct.Struct("PACKET_F_DO_ABILITY",
    # TODO
    )

F_SET_TIME = 0xD6
SIZE_PACKET_F_SET_TIME = 0x00 # TODO
PACKET_F_SET_TIME = construct.Struct("PACKET_F_SET_TIME",
    # TODO
    )

F_INIT_EFFECTS = 0xD7
SIZE_PACKET_F_INIT_EFFECTS = 0x00 # TODO
PACKET_F_INIT_EFFECTS = construct.Struct("PACKET_F_INIT_EFFECTS",
    # TODO
    )

F_GROUP_STATUS = 0xD8
SIZE_PACKET_F_GROUP_STATUS = 0x00 # TODO
PACKET_F_GROUP_STATUS = construct.Struct("PACKET_F_GROUP_STATUS",
    # TODO
    )

F_USE_ITEM = 0xD9
SIZE_PACKET_F_USE_ITEM = 0x00 # TODO
PACKET_F_USE_ITEM = construct.Struct("PACKET_F_USE_ITEM",
    # TODO
    )

F_USE_ABILITY = 0xDA
SIZE_PACKET_F_USE_ABILITY = 0x00 # TODO
PACKET_F_USE_ABILITY = construct.Struct("PACKET_F_USE_ABILITY",
    # TODO
    )

F_INFLUENCE_DETAILS = 0xDB
SIZE_PACKET_F_INFLUENCE_DETAILS = 0x00 # TODO
PACKET_F_INFLUENCE_DETAILS = construct.Struct("PACKET_F_INFLUENCE_DETAILS",
    # TODO
    )

F_BUG_REPORT = 0xDD
SIZE_PACKET_F_BUG_REPORT = 0x00 # TODO
PACKET_F_BUG_REPORT = construct.Struct("PACKET_F_BUG_REPORT",
    # TODO
    )

F_OBJECT_EFFECT_STATE = 0xDE
SIZE_PACKET_F_OBJECT_EFFECT_STATE = 0x00 # TODO
PACKET_F_OBJECT_EFFECT_STATE = construct.Struct("PACKET_F_OBJECT_EFFECT_STATE",
    # TODO
    )

F_EXPERIENCE_TABLE = 0xE2
SIZE_PACKET_F_EXPERIENCE_TABLE = 0x00 # TODO
PACKET_F_EXPERIENCE_TABLE = construct.Struct("PACKET_F_EXPERIENCE_TABLE",
    # TODO
    )

F_CREATE_PLAYER = 0xE3
SIZE_PACKET_F_CREATE_PLAYER = 0x00 # TODO
PACKET_F_CREATE_PLAYER = construct.Struct("PACKET_F_CREATE_PLAYER",
    # TODO
    )

F_UPDATE_STATE = 0xE4
SIZE_PACKET_F_UPDATE_STATE = 0x00 # TODO
PACKET_F_UPDATE_STATE = construct.Struct("PACKET_F_UPDATE_STATE",
    # TODO
    )

F_UI_MOD = 0xE5
SIZE_PACKET_F_UI_MOD = 0x00 # TODO
PACKET_F_UI_MOD = construct.Struct("PACKET_F_UI_MOD",
    # TODO
    )

F_RVR_STATS = 0xE7
SIZE_PACKET_F_RVR_STATS = 0x00 # TODO
PACKET_F_RVR_STATS = construct.Struct("PACKET_F_RVR_STATS",
    # TODO
    )

F_CLIENT_DATA = 0xE8
SIZE_PACKET_F_CLIENT_DATA = 0x00 # TODO
PACKET_F_CLIENT_DATA = construct.Struct("PACKET_F_CLIENT_DATA",
    # TODO
    )

F_INTERACT_RESPONSE = 0xE9
SIZE_PACKET_F_INTERACT_RESPONSE = 0x00 # TODO
PACKET_F_INTERACT_RESPONSE = construct.Struct("PACKET_F_INTERACT_RESPONSE",
    # TODO
    )

F_QUEST_LIST = 0xEA
SIZE_PACKET_F_QUEST_LIST = 0x00 # TODO
PACKET_F_QUEST_LIST = construct.Struct("PACKET_F_QUEST_LIST",
    # TODO
    )

F_QUEST_UPDATE = 0xEB
SIZE_PACKET_F_QUEST_UPDATE = 0x00 # TODO
PACKET_F_QUEST_UPDATE = construct.Struct("PACKET_F_QUEST_UPDATE",
    # TODO
    )

F_REQUEST_QUEST = 0xEC
SIZE_PACKET_F_REQUEST_QUEST = 0x00 # TODO
PACKET_F_REQUEST_QUEST = construct.Struct("PACKET_F_REQUEST_QUEST",
    # TODO
    )

F_QUEST_LIST_UPDATE = 0xED
SIZE_PACKET_F_QUEST_LIST_UPDATE = 0x00 # TODO
PACKET_F_QUEST_LIST_UPDATE = construct.Struct("PACKET_F_QUEST_LIST_UPDATE",
    # TODO
    )

F_CAREER_CATEGORY = 0xEE
SIZE_PACKET_F_CAREER_CATEGORY = 0x00 # TODO
PACKET_F_CAREER_CATEGORY = construct.Struct("PACKET_F_CAREER_CATEGORY",
    # TODO
    )

F_CAREER_PACKAGE_UPDATE = 0xF1
SIZE_PACKET_F_CAREER_PACKAGE_UPDATE = 0x00 # TODO
PACKET_F_CAREER_PACKAGE_UPDATE = construct.Struct("PACKET_F_CAREER_PACKAGE_UPDATE",
    # TODO
    )

F_BUY_CAREER_PACKAGE = 0xF2
SIZE_PACKET_F_BUY_CAREER_PACKAGE = 0x00 # TODO
PACKET_F_BUY_CAREER_PACKAGE = construct.Struct("PACKET_F_BUY_CAREER_PACKAGE",
    # TODO
    )

F_CAREER_PACKAGE_INFO = 0xF3
SIZE_PACKET_F_CAREER_PACKAGE_INFO = 0x00 # TODO
PACKET_F_CAREER_PACKAGE_INFO = construct.Struct("PACKET_F_CAREER_PACKAGE_INFO",
    # TODO
    )

F_DO_ABILITY_AT_POS = 0xF5
SIZE_PACKET_F_DO_ABILITY_AT_POS = 0x00 # TODO
PACKET_F_DO_ABILITY_AT_POS = construct.Struct("PACKET_F_DO_ABILITY_AT_POS",
    # TODO
    )

F_CHANNEL_LIST = 0xF6
SIZE_PACKET_F_CHANNEL_LIST = 0x00 # TODO
PACKET_F_CHANNEL_LIST = construct.Struct("PACKET_F_CHANNEL_LIST",
    # TODO
    )

F_TACTICS = 0xF7
SIZE_PACKET_F_TACTICS = 0x00 # TODO
PACKET_F_TACTICS = construct.Struct("PACKET_F_TACTICS",
    # TODO
    )

F_TOK_ENTRY_UPDATE = 0xF8
SIZE_PACKET_F_TOK_ENTRY_UPDATE = 0x00 # TODO
PACKET_F_TOK_ENTRY_UPDATE = construct.Struct("PACKET_F_TOK_ENTRY_UPDATE",
    # TODO
    )

F_RENDER_PRIMITIVE = 0xFA
SIZE_PACKET_F_RENDER_PRIMITIVE = 0x00 # TODO
PACKET_F_RENDER_PRIMITIVE = construct.Struct("PACKET_F_RENDER_PRIMITIVE",
    # TODO
    )

F_INFLUENCE_UPDATE = 0xFB
SIZE_PACKET_F_INFLUENCE_UPDATE = 0x00 # TODO
PACKET_F_INFLUENCE_UPDATE = construct.Struct("PACKET_F_INFLUENCE_UPDATE",
    # TODO
    )

F_INFLUENCE_INFO = 0xFC
SIZE_PACKET_F_INFLUENCE_INFO = 0x00 # TODO
PACKET_F_INFLUENCE_INFO = construct.Struct("PACKET_F_INFLUENCE_INFO",
    # TODO
    )

F_KNOCKBACK = 0xFD
SIZE_PACKET_F_KNOCKBACK = 0x00 # TODO
PACKET_F_KNOCKBACK = construct.Struct("PACKET_F_KNOCKBACK",
    # TODO
    )

F_PLAY_VOICE_OVER = 0xFE
SIZE_PACKET_F_PLAY_VOICE_OVER = 0x00 # TODO
PACKET_F_PLAY_VOICE_OVER = construct.Struct("PACKET_F_PLAY_VOICE_OVER",
    # TODO
    )