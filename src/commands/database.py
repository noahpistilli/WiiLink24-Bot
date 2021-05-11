import psycopg2


def check_user(username, user_id, check_ban, reason, muted):
    global strikes
    connection = psycopg2.connect(user="user",
                                  password="pass",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * from userinfo WHERE userid = {user_id}")
    record = cursor.fetchall()

    if len(record) > 0:
        for row in record:
            strikes = row[1]
    else:
        strikes = 0

    return f":white_check_mark: Moderation Information for **{username}** (ID:{user_id}): " \
           f"\n:triangular_flag_on_post: Strikes: **{strikes}**\n:mute: Muted: **{muted}**\n:hammer: Banned: **{check_ban}** {reason}"
