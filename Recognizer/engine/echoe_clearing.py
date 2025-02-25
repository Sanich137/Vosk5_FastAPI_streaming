import trash.test_data
from typing import List, Dict, Any



async def remove_echo(input_json: Dict[str, List[Dict[str, Any]]], delta: float = 0.4) -> Dict[str, List[Dict[str, Any]]]:
    output_json = {}

    # Получаем список каналов
    channels = list(input_json.keys())

    # Создаём копию входных данных для изменений
    for channel_name in channels:
        output_json[channel_name] = [msg.copy() for msg in input_json[channel_name]]

    # Проходим по всем каналам
    for i, channel_name in enumerate(channels):
    #for i, channel_name in enumerate(reversed(channels)):
        for message in output_json[channel_name]:
            if not message.get("silence", False):  # Игнорируем тишину
                # Создаём список для хранения слов, которые не являются эхом
                cleaned_words = []

                for word in message["data"]["result"]:
                    is_echo = False

                    # Проверяем другие каналы
                    for other_channel_name in channels:
                        if other_channel_name != channel_name:  # Игнорируем текущий канал
                            for other_message in output_json[other_channel_name]:
                                if not other_message.get("silence", False):  # Игнорируем тишину
                                    for other_word in other_message["data"]["result"]:
                                        # Проверяем, находится ли слово в пределах дельты до или после текущего слова
                                        if abs(word["end"] - other_word["end"]) <= delta and word["word"] == other_word["word"]:
                                            # Если слово найдено до текущего, удаляем его из текущего канала
                                            if other_word["end"] < word["end"]:
                                                is_echo = True

                                                print(f"<--- слово '{word['word']}' найдено до текущего, удаляем его из текущего канала")
                                                print(f"В текущем канале время {word['end']}")
                                                print(f"В другом канале время {word['end']}")


                                                break
                                            # Если слово найдено после текущего, удаляем его из другого канала
                                            elif other_word["end"] > word["end"]:
                                                other_message["data"]["result"].remove(other_word)
                                                other_message["data"]["text"] = " ".join(
                                                    [w["word"] for w in other_message["data"]["result"]]
                                                )
                                                print(
                                                    f"---> слово '{word['word']}' найдено после текущего, удаляем его из другого канала")
                                    if is_echo:
                                        break
                            if is_echo:
                                break

                    # Если слово не является эхом, добавляем его в очищенный список
                    if not is_echo:
                        cleaned_words.append(word)

                # Обновляем результат и текст в текущем сообщении
                message["data"]["result"] = cleaned_words
                message["data"]["text"] = " ".join([w["word"] for w in cleaned_words])

    return output_json



if __name__ == "__main__":

    input_data = trash.test_data.for_echo["raw_data"]
    print(remove_echo(input_data))




