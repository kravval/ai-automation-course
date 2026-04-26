"""
Задача 1: zero-shot извлечение метаданных книг с piter.com.
Цель — освоить зрелый zero-shot промпт и итеративный цикл улучшения.
"""
import os
import json
from dotenv import load_dotenv
import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1000
TEMPERATURE = 0

SYSTEM_PROMPT = """
    Ты — IT-библиотекарь и технический рецензент. 
    Ты специализируешься на каталогизации технической литературы для разработчиков. Т
    ы хорошо разбираешься в IT-книгах разных издательств (Питер, O'Reilly, Manning, Apress) и умеешь точно классифицировать книги по уровню читателя и тематике.
    
    ЗАДАЧА:
    Извлеки структурированные метаданные из описания книги и верни их в JSON-формате.
    
    КРИТИЧЕСКИ ВАЖНЫЕ ПРАВИЛА:
    1. Поля title, authors, year — это ИЗВЛЕКАЕМЫЕ ФАКТЫ.
   Бери их ТОЛЬКО из текста описания, дословно. НИКОГДА не используй свои
   знания о конкретных книгах из памяти. Если поле невозможно извлечь
   из текста — используй null или пустой массив. Не догадывайся.

    2. Поля topics и level — это ВЫВОДЫ ИЗ СОДЕРЖАНИЯ.
   Их нужно определить, проанализировав, о чём идёт речь в описании.
   Опирайся на ключевые слова, технологии, формулировки в тексте.
   Если описание слишком общее, чтобы определить уровень с уверенностью —
   ставь "intermediate" как нейтральный по умолчанию.
    
    ФОРМАТ ОТВЕТА (СТРОГО JSON, без markdown-обёрток):
    {
      "title": "название книги (string)",
      "authors": ["имя автора как упомянуто в тексте (string)", ...],
      "year": год издания (number, 4 цифры) или null,
      "topics": ["тема (string, lowercase, на английском, кратко 1-2 слова)", ...],
      "level": "beginner" | "intermediate" | "advanced"
    }
    
    ПРАВИЛА ДЛЯ ПОЛЕЙ:
    
    - title: точное название книги, как в описании.
    - authors: список авторов, упомянутых в тексте описания. Если в описании нет упоминания авторов — пустой массив []. 
    НЕ добавляй авторов из своих знаний о книге.
    - year: только если год явно указан в тексте описания. Иначе null.
    - topics: 3-6 ключевых тем книги. На английском, lowercase, краткие (1-2 слова): "java", "concurrency", "microservices", "spring boot", "kafka", "streaming", "testing", "architecture".
    - level: уровень читателя книги. Определи по содержанию:
      * "beginner" — основы языка/технологии, для начинающих, без предварительного опыта.
      * "intermediate" — для разработчиков с базовым опытом, практическое применение технологий.
      * "advanced" — углублённые темы, для профессионалов, сложные паттерны, оптимизация, архитектурные решения.
    
    Не добавляй полей, которых нет в схеме. Не оборачивай ответ в markdown. Только чистый JSON.
    """

SAMPLES = [
    {
        "url": "https://www.piter.com/collection/all/product/java-concurrency-na-praktike",  # ← подставь реальный URL
        "description": """
 Потоки являются фундаментальной частью платформы Java. 
 Многоядерные процессоры — это обыденная реальность, а эффективное использование параллелизма стало необходимым для создания любого высокопроизводительного приложения. Улучшенная виртуальная машина Java, поддержка высокопроизводительных классов и богатый набор строительных блоков для задач распараллеливания стали в свое время прорывом в разработке параллельных приложений. В «Java Concurrency на практике» сами создатели прорывной технологии объясняют не только принципы работы, но и рассказывают о паттернах проектирования.

Легко создать конкурентную программу, которая вроде бы будет работать. Однако разработка, тестирование и отладка многопоточных программ доставляют много проблем. Код перестает работать именно тогда, когда это важнее всего — при большой нагрузке. В «Java Concurrency на практике» вы найдете как теорию, так и конкретные методы создания надежных, масштабируемых и поддерживаемых параллельных приложений. Авторы не предлагают перечень API и механизмов параллелизма, они знакомят с правилами проектирования, паттернами и моделями, которые не зависят от версии Java и на протяжении многих лет остаются актуальными и эффективными.

Эта книга охватывает следующие темы:

- Базовые концепции параллелизма и безопасности потоков
- Методы построения и составления многопоточных классов
- Использование блоков параллелизма в java.util.concurrent
- Оптимизация производительности: что можно делать, а что не стоит и пытаться
- Тестирование параллельных программ
- Атомарные переменные, неблокирующие алгоритмы и модель памяти Java
            """,
        "expected": {
            "title": "Java Concurrency на практике",
            "authors": [],
            "year": None,
            "level": "advanced",
            # темы (topics) пока не указываем в эталоне —
            # для тем оценим визуально, без жёсткого сравнения
        }
    },
    {
        "url": "http://piter.com/collection/all/product/mikroservisy-patterny-razrabotki-i-refaktoringa",
        # ← подставь реальный URL
        "description": """
           Если вам давно кажется, что вся разработка и развертывание в вашей компании донельзя замедлились – переходите на микросервисную архитектуру. Она обеспечивает непрерывную разработку, доставку и развертывание приложений любой сложности.
Книга, предназначенная для разработчиков и архитекторов из больших корпораций, рассказывает, как проектировать и писать приложения в духе микросервисной архитектуры. Также в ней описано, как делается рефакторинг крупного приложения – и монолит превращается в набор микросервисов.
В этой книге
 Как (и зачем!) использовать микросервисную архитектуру.
 Стратегии декомпозиции сервисов.
 Управление транзакциями и шаблоны запросов.
 Эффективные стратегии тестирования.
 Шаблоны развертывания, включая контейнеры и бессерверные платформы.
            """,
        "expected": {
            "title": "Микросервисы. Паттерны разработки и рефакторинга",
            "authors": [],
            "year": None,
            "level": "advanced",
            # темы (topics) пока не указываем в эталоне —
            # для тем оценим визуально, без жёсткого сравнения
        }
    },
    {
        "url": "https://www.piter.com/collection/java/product/spring-boot-po-bystromu",  # ← подставь реальный URL
        "description": """
Spring Boot, который скачивают более 75 миллионов раз в месяц, — наиболее широко используемый фреймворк Java. 
Его удобство и возможности совершили революцию в разработке приложений, от монолитных до микросервисов. 
Тем не менее простота Spring Boot может привести в замешательство. 
Что именно разработчику нужно изучить, чтобы сразу же выдавать результат? 
Это практическое руководство научит вас писать успешные приложения для критически важных задач.
Марк Хеклер из VMware, компании, создавшей Spring, проведет вас по всей архитектуре Spring Boot, охватив такие вопросы, 
как отладка, тестирование и развертывание. Если вы хотите быстро и эффективно разрабатывать нативные облачные 
приложения Java или Kotlin на базе Spring Boot с помощью реактивного программирования, создания API и доступа к 
разнообразным базам данных — эта книга для вас.
            """,
        "expected": {
            "title": "Spring Boot по-быстрому",
            "authors": ["Марк Хеклер"],
            "year": None,
            "level": "intermediate",
            # темы (topics) пока не указываем в эталоне —
            # для тем оценим визуально, без жёсткого сравнения
        }
    },

    {
        "url": "https://www.piter.com/collection/all/product/kafka-streams-i-ksqldb-dannye-v-realnom-vremeni",
        # ← подставь реальный URL
        "description": """
Работа с неограниченными и быстрыми потоками данных всегда была сложной задачей. 
Но Kafka Streams и ksqlDB позволяют легко и просто создавать приложения потоковой обработки. 
Из книги специалисты по обработке данных узнают, как с помощью этих инструментов создавать 
масштабируемые приложения потоковой обработки, перемещающие, обогащающие и преобразующие большие объемы 
данных в режиме реального времени.
Митч Сеймур, инженер службы обработки данных в Mailchimp, объясняет важные понятия потоковой 
обработки на примере нескольких любопытных бизнес-задач. Он рассказывает о достоинствах Kafka Streams и ksqlDB, 
чтобы помочь вам выбрать наиболее подходящий инструмент для каждого уникального проекта потоковой обработки. 
Для разработчиков, не пишущих код на Java, особенно ценным будет материал, посвященный ksqlDB.
            """,
        "expected": {
            "title": "Kafka Streams и ksqlDB: данные в реальном времени",
            "authors": ["Митч Сеймур"],
            "year": None,
            "level": "advanced",
            # темы (topics) пока не указываем в эталоне —
            # для тем оценим визуально, без жёсткого сравнения
        }
    },
]


def strip_code_fences(text: str) -> str:
    """Убирает markdown-обёртку ```...``` вокруг ответа модели."""
    text = text.strip()
    if text.startswith("```"):
        if "\n" in text:
            text = text.split("\n", 1)[1]
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
    return text.strip()

def validate_book_metadata(data: dict) -> None:
    """
    Проверяет структуру распарсенных метаданных книги.
    Бросает ValueError при ошибке.
    """

    if "title" not in data:
        raise ValueError("Отсутствует поле 'title'")
    if not isinstance(data["title"], str) or not data["title"].strip():
        raise ValueError("Поле 'title' должно быть непустой строкой")
    if "authors" not in data:
        raise ValueError("Отсутствует поле 'authors'")
    if not isinstance(data["authors"], list):
        raise ValueError("Поле 'authors' должно быть массивом")
    if not all(isinstance(a, str) for a in data["authors"]):
        raise ValueError("Все элементы 'authors' должны быть строками")
    if "year" not in data:
        raise ValueError("Отсутствует поле 'year'")
    if data["year"] is not None and not isinstance(data["year"], int):
        raise ValueError("Поле 'year' должно быть числом или null")
    if "topics" not in data:
        raise ValueError("Отсутствует поле 'topics'")
    if not isinstance(data["topics"], list):
        raise ValueError("Поле 'topics' должно быть массивом")

    if "level" not in data:
        raise ValueError("Отсутствует поле 'level'")
    allowed_levels = {"beginner", "intermediate", "advanced"}
    if data["level"] not in allowed_levels:
        raise ValueError(f"Поле 'level' должно быть одним из {allowed_levels}, "
                         f"получено: '{data['level']}'")


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((
            anthropic.RateLimitError,
            anthropic.APIConnectionError,
            anthropic.APIStatusError
    )),
    reraise=True
)
def call_llm(client: anthropic.Anthropic, system_prompt: str, user_message: str) -> str:
    """
    Вызывает Claude и возвращает текст ответа.
    Повторяется при временных ошибках.
    """
    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    return message.content[0].text


def extract_book_metadata(client: anthropic.Anthropic, description: str) -> dict:
    """
    Извлекает структурированные метаданные книги из описания.

    Args:
        client: клиент Anthropic API
        description: текст описания книги

    Returns:
        dict с полями: title, authors, year, topics, level

    Raises:
        anthropic.APIError, json.JSONDecodeError, ValueError
    """
    user_message = f"Извлеки метаданные из следующего описания книги:\n\n{description}"

    raw_response = call_llm(client, SYSTEM_PROMPT, user_message)
    cleaned_response = strip_code_fences(raw_response)
    data = json.loads(cleaned_response)
    validate_book_metadata(data)

    return data

def main():
    """Точка входа: обрабатывает первый образец и печатает результат."""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    sample = SAMPLES[2]
    print(f"Обрабатываю: {sample['url']}\n ")
    try:
        result = extract_book_metadata(client, sample["description"])
    except anthropic.AuthenticationError:
        print("❌ Ошибка авторизации: проверь API-ключ в .env")
        raise SystemExit(1)
    except anthropic.APIError as e:
        print(f"❌ Ошибка API: {e}")
        raise SystemExit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Модель вернула невалидный JSON: {e}")
        raise SystemExit(1)
    except ValueError as e:
        print(f"❌ Ошибка валидации: {e}")
        raise SystemExit(1)

    print("=== Результат ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
