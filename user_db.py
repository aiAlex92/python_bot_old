from time import time
from pytz import timezone

from datetime import datetime
from replit import db

moscow_tz = timezone('Europe/Moscow')

class User():
  def __init__(self, user_id):
    self.user_id = user_id

  def __str__(self):
    dt = datetime.fromtimestamp(self.get_start_timestamp(), tz=moscow_tz)
    human_dt = dt.strftime("%d.%m.%Y, %H:%M:%S")        
    return f"User {self.user_id} ({self.get_full_name()})\nStart time: {human_dt}"

  def set_full_name(self, full_name: str) -> None:
    db[f"full_name:{self.user_id}"] = full_name

  def get_full_name(self) -> str:
    return db.get(f"full_name:{self.user_id}", "")

  def set_city(self, city: str) -> None:
    db[f"city:{self.user_id}"] = city

  def get_city(self) -> str:
    return db.get(f"city:{self.user_id}", "")
  
  def set_age(self, age: int) -> None:
    db[f"age:{self.user_id}"] = age

  def get_age(self) -> [int, None]:
    return db.get(f"age:{self.user_id}")
  
  def set_ms(self, ms: str) -> None:
    db[f"ms:{self.user_id}"] = ms

  def get_ms(self) -> str:
    return db.get(f"ms:{self.user_id}", "")

  def set_step(self, step: str) -> None:
    db[f"step:{self.user_id}"] = step

  def get_step(self) -> str:
    return db.get(f"step:{self.user_id}", "age")

  def start(self):
    # Сохраняем время и дату старта
    if f"start:{self.user_id}" not in db:
      db[f"start:{self.user_id}"] = int(time())

  def reset(self):
    del db[f"step:{self.user_id}"]
    del db[f"age:{self.user_id}"]
    del db[f"city:{self.user_id}"]
    del db[f"ms:{self.user_id}"]

  def get_start_timestamp(self):
    return db.get(f"start:{self.user_id}", 0)


if __name__ == "__main__":
  p = print