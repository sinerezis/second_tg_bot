import sqlite3

class SQLighter:


    def __init__(self, database):
        """Connect to db"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        """get all active subscribers"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exist(self, user_id):
        """try found user in database"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=True):
        """add new user"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions`(`user_id`, `status`) VALUES (?,?)", (user_id, status))

    def update_subscriptions(self, user_id, status):
        """refresh subscr status"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` =?", (status, user_id))

    def close(self):
        """close connection"""
        self.connection.close()



# import sqlite3

# class SQLighter:

#     def __init__(self, database):
#         """Подключаемся к БД и сохраняем курсор соединения"""
#         self.connection = sqlite3.connect(database)
#         self.cursor = self.connection.cursor()

#     def get_subscriptions(self, status = True):
#         """Получаем всех активных подписчиков бота"""
#         with self.connection:
#             return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    # def subscriber_exist(self, user_id):
    #     """Проверяем, есть ли уже юзер в базе"""
    #     with self.connection:
    #         result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
    #         return bool(len(result))

#     def add_subscriber(self, user_id, status = True):
#         """Добавляем нового подписчика"""
#         with self.connection:
#             return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

#     def update_subscriptions(self, user_id, status):
#         """Обновляем статус подписки пользователя"""
#         with self.connection:
#             return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

#     def close(self):
#         """Закрываем соединение с БД"""
#         self.connection.close()