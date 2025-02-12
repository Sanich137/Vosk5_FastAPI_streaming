> Сервер для Распознавания на базе FastAPI + Vosk 5 версии.

- В работе можно будет использовать три версии - small-streaming, vosk-model-ru и gigaam. Сейчас используется vosk-model-ru.  
- Отличия в работе. 
  - Стриминговая версия с каждым новым чанком **будет** отдавать текст с накоплением. Говорят, оно работает быстрее.
  на самом деле Sherpa-onnx настолько быстр, что разницы быть не должно.
  - Полная версия в реализации интересна написанным буфером аудио потока. Технически с каждым новым чанком 
  мы отсекаем последние микрочанки с голосом и отправляем на распознавание всё остальное. И, если вдруг весь чанк 
  это голос, то копим чанки в один мегачанк, но не более чем 15 секунд т.к. большая модель за один стрим есть только 18. 
  - gigaam пока не запускал

> FastApi используется в т.ч. для проверки входящих запросов, возможно, для выполнения дополнительных инструкций,
таких как постобработка текста, история запросов и м.б. что-то ещё чего прикручу.

> Модели:
> - большая https://huggingface.co/alphacep/vosk-model-ru
> - малая   https://huggingface.co/alphacep/vosk-model-small-ru
> - Gigaam [инструкция по получению onnx от Sber](https://github.com/salute-developers/GigaAM/blob/main/inference_example.ipynb)
> - Gigaam [Инструкция от @nshmyrev](https://k2-fsa.github.io/sherpa/onnx/pretrained_models/offline-ctc/nemo/russian.html#sherpa-onnx-nemo-ctc-giga-am-russian-2024-10-24)
> - [Лицензия Gigaam](https://github.com/salute-developers/GigaAM/blob/main/GigaAM%20License_NC.pdf) не допускает коммерческого использования. 

По умолчанию приложение работает на CPU. Как следствие с увеличением количества запросов время подготовки ответа растёт.

Установка:

Если GPU не нужен, то не выполняем пункты до Ставим основной пакет.

> Для поддержки GPU на линукс: 
> Ставим Cuda 11.8 и cudNN к ней [по инструкции:](https://k2-fsa.github.io/k2/installation/cuda-cudnn.html#cuda-11-8) 

```commandline
sudo apt update && apt upgrade -y
sudo apt install gcc
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run &&
chmod +x cuda_11.8.0_520.61.05_linux.run
sudo ./cuda_11.8.0_520.61.05_linux.run \
   --silent \
  --toolkit \
  --installpath=/usr/local/cuda-11.8.0 \
  --no-opengl-libs \
  --no-drm \
  --no-man-page \
  --override
wget https://huggingface.co/csukuangfj/cudnn/resolve/main/cudnn-linux-x86_64-8.9.1.23_cuda11-archive.tar.xz
sudo tar xvf cudnn-linux-x86_64-8.9.1.23_cuda11-archive.tar.xz --strip-components=1 -C /usr/local/cuda-11.8.0
```

Если у Вас установлено несколько версий CUDA, 
то используем файл для переключения на cuda 11.8 [activate-cuda-11.8.sh](activate-cuda-11.8.sh) 
и переключаем на него:
```commandline
source activate-cuda-11.8.sh
```

- Ставим основной пакет (не забываем инициировать и активировать виртуальное окружение).
```commandline
pip install -r requirements.txt
sudo apt-get install -y git-lfs
sudo apt install -y ffmpeg
```
Не забываем поставить git-lfs и ffmpeg [Детали тут](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage?platform=windows)
 [или тут](https://github.com/git-lfs/git-lfs/blob/main/INSTALLING.md). Если не поставить, то получите ошибку: RuntimeError: Failed to load model because protobuf parsing failed.

```commandline
sudo apt-get install git-lfs
```

- Затем копируем модель в папку:
```commandline
cd models
git clone https://huggingface.co/alphacep/vosk-model-ru
cd ..
```

- Запуск приложения:

```commandline
python3 main.py
```
 
- В окружение добавляем переменные:

```LOGGING_LEVEL = INFO``` (уровень логирования - по умолчанию DEBUG)

```NUM_THREADS = 2``` (количество потоков на распознавание. Нормально работает от двух и выше.)

```HOST = "0.0.0.0.0"``` 

```PORT = "49153"```

- Запускаем приложение:
```commandline
source venv
```

- Проверяем запуск на 
```commandline
http://127.0.0.1:49153/docs#/
``` 

-  Для тестирования можно использовать - [WS_Test.py](WS_Test.py)


> Если используем приложение как service в ubuntu, то поможет пример файла [.service](vosk_gpu.service) 
c активацией нужных переменных CUDA. Не забудьте изменить имя пользователя в файле и поместить его в:
```commandline
cd /etc/systemd/system
```

запустить сервис: 

```commandline
sudo systemctl start vosk_gpu
```

Проверить как он работает:
```commandline
journalctl -eu vosk_gpu -f
```
И, если всё ОК, то включить его в автозагрузку:
```commandline
sudo systemctl enable vosk_gpu
```
