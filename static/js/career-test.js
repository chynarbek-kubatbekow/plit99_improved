document.addEventListener('DOMContentLoaded', () => {
  const root = document.querySelector('[data-career-test]');
  if (!root) return;

  const clusters = {
    dev: {
      title: 'Dev / IT-Core',
      programs: ['Фронтенд', 'Бэкенд', 'Веб-разработка', 'Мобильная разработка'],
      interestText: 'нужно выстроить внутреннюю логику, собрать понятную систему и довести ее до рабочего состояния',
      reality: [
        'Собирать сайты, приложения, формы и интерактивные элементы.',
        'Искать ошибки, проверять логику и улучшать поведение страниц.',
        'Разбивать большую задачу на шаги и доводить решение до результата.',
      ],
      tenMinutes: 'Открой любую страницу сайта лицея и выпиши 3 вещи, которые можно сделать понятнее или быстрее для пользователя.',
      caseName: 'сайтом лицея',
    },
    infra: {
      title: 'Infra / Security',
      programs: ['Системное администрирование', 'Кибербезопасность'],
      interestText: 'важна стабильность, порядок, диагностика причин и спокойная проверка каждого звена',
      reality: [
        'Настраивать компьютеры, сеть, учетные записи и доступы.',
        'Проверять, почему пропал интернет или сервис работает нестабильно.',
        'Думать о безопасности, резервных копиях и аккуратных инструкциях.',
      ],
      tenMinutes: 'Нарисуй схему домашнего интернета: роутер, устройства, Wi-Fi, кабели. Отметь, где первым делом проверил бы сбой.',
      caseName: 'компьютерным классом',
    },
    creative: {
      title: 'Creative / Design',
      programs: ['Технологии дизайна', 'Дизайн одежды'],
      interestText: 'есть тяга к форме, цвету, композиции, образу и тому, как идея выглядит для других людей',
      reality: [
        'Создавать афиши, макеты, визуальные материалы, 3D и motion-элементы.',
        'Подбирать стиль, композицию, цвет и шрифт под задачу.',
        'Переделывать работу после обратной связи и объяснять свои решения.',
      ],
      tenMinutes: 'Сделай быстрый набросок афиши Дня открытых дверей: заголовок, главный визуальный акцент и 2 цвета.',
      caseName: 'Днем открытых дверей',
    },
    engineering: {
      title: 'Engineering / Tech',
      programs: ['Мехатроника', 'Горное оборудование'],
      interestText: 'интересно понимать, как части связаны между собой, почему механизм работает и где нарушилась цепочка',
      reality: [
        'Собирать и проверять учебные стенды, датчики, лампы, двигатели и узлы.',
        'Разбираться, какая часть схемы или конструкции мешает работе.',
        'Соединять физику, механику, электрические сигналы и практическую проверку.',
      ],
      tenMinutes: 'Возьми любой предмет с подвижной частью и опиши, какие узлы заставляют его работать.',
      caseName: 'учебным стендом',
    },
    mechanics: {
      title: 'Mechanics / Practice',
      programs: ['Автоэлектрик', 'Практическая диагностика техники'],
      interestText: 'тянет к реальным устройствам, инструментам, проверке контактов, деталей и ощутимому результату руками',
      reality: [
        'Диагностировать неисправности в учебных авто, агрегатах и электрических элементах.',
        'Работать с инструментом, схемами, измерениями и заменой деталей.',
        'Проверять результат на реальном устройстве, а не только в теории.',
      ],
      tenMinutes: 'Выбери любой бытовой прибор и составь безопасный список проверок: питание, кабель, кнопка, видимые повреждения.',
      caseName: 'учебным авто',
    },
  };

  const interestQuestions = [
    {
      text: 'В классе готовите общий проект для мероприятия. К чему ты скорее всего подключишься?',
      options: [
        ['dev', 'Собрать форму, таблицу или простой порядок, чтобы ответы людей потом было легко посчитать.'],
        ['infra', 'Разобраться, почему техника в кабинете не подключается или показывает материалы с перебоями.'],
        ['creative', 'Продумать афишу, слайды, обложку или общий визуальный стиль проекта.'],
        ['engineering', 'Придумать макет, стенд или небольшую конструкцию, которая что-то показывает вживую.'],
        ['mechanics', 'Починить колонку, провод, крепление или другую вещь, без которой проект не запустится.'],
      ],
    },
    {
      text: 'В групповой домашке всем нужно разделить роли. Какая роль для тебя звучит наиболее естественно?',
      options: [
        ['dev', 'Собрать общий результат в понятную систему, чтобы ничего не потерялось и работало по шагам.'],
        ['infra', 'Проверить, у всех ли есть доступы, файлы, устройства и нормальная связь для работы.'],
        ['creative', 'Сделать так, чтобы итог выглядел цельно, аккуратно и его было приятно показывать.'],
        ['engineering', 'Понять, как устроить модель или опыт, чтобы он был не только красивым, но и рабочим.'],
        ['mechanics', 'Взять на себя сборку, проверку деталей и исправление того, что не держится или не включается.'],
      ],
    },
    {
      text: 'О чем тебя чаще просит окружение, когда нужно помочь?',
      options: [
        ['dev', 'Придумать удобный способ посчитать, отсортировать или автоматизировать повторяющиеся действия.'],
        ['infra', 'Понять, почему устройство, аккаунт, интернет или программа ведут себя странно.'],
        ['creative', 'Подобрать оформление, картинку, образ, цвет или сделать материал более выразительным.'],
        ['engineering', 'Объяснить, как работает механизм, схема, датчик или вещь с несколькими связанными частями.'],
        ['mechanics', 'Посмотреть реальную поломку: контакт, провод, крепление, лампу, кнопку или двигатель.'],
      ],
    },
    {
      text: 'Представь школьную ярмарку идей. Какой уголок ты бы выбрал для себя?',
      options: [
        ['dev', 'Где участники придумывают правила работы интерактивной системы и проверяют, не ломается ли логика.'],
        ['infra', 'Где нужно наладить порядок: устройства, доступ, соединения, безопасность и инструкции.'],
        ['creative', 'Где делают визуальную подачу, постеры, стиль, образы и короткие анимации.'],
        ['engineering', 'Где собирают стенд с датчиками, лампочками, движением или измерениями.'],
        ['mechanics', 'Где разбирают реальные узлы, проверяют детали и возвращают технику в рабочее состояние.'],
      ],
    },
    {
      text: 'Какой тип задач тебе легче долго выдерживать?',
      options: [
        ['dev', 'Долго искать, где нарушилась логика, пока система наконец не начинает вести себя правильно.'],
        ['infra', 'Методично проверять цепочку причин: питание, подключение, настройки, доступы, нагрузку.'],
        ['creative', 'Перебирать варианты формы, цвета, ритма и композиции, пока результат не станет точнее.'],
        ['engineering', 'Настраивать узел или модель, где маленькое изменение влияет на всю работу.'],
        ['mechanics', 'Проверять руками, прибором или на слух, какая деталь мешает нормальной работе.'],
      ],
    },
    {
      text: 'Когда что-то ломается, что ты чаще делаешь первым делом?',
      options: [
        ['dev', 'Вспоминаю последние изменения и пытаюсь найти шаг, после которого все пошло не так.'],
        ['infra', 'Проверяю простые причины по порядку и отделяю проблему устройства от проблемы окружения.'],
        ['creative', 'Смотрю, не мешает ли восприятию лишняя деталь, неудачный акцент или плохая подача.'],
        ['engineering', 'Разбираю, какая часть системы связана с неисправной частью и как они влияют друг на друга.'],
        ['mechanics', 'Осматриваю контакты, крепления, питание, следы износа и то, что можно проверить физически.'],
      ],
    },
    {
      text: 'Если неделю делать маленький проект, что меньше всего тебя утомит?',
      options: [
        ['dev', 'Каждый день улучшать внутреннюю структуру и исправлять ошибки в поведении системы.'],
        ['infra', 'Каждый день делать среду стабильнее, понятнее и защищеннее от случайных сбоев.'],
        ['creative', 'Каждый день пробовать новые версии одной идеи и доводить визуальный результат.'],
        ['engineering', 'Каждый день дорабатывать конструкцию или схему, чтобы она работала надежнее.'],
        ['mechanics', 'Каждый день проверять разные реальные устройства, находить причины и устранять мелкие неисправности.'],
      ],
    },
    {
      text: 'В сложной задаче тебе обычно приятнее, когда получается...',
      options: [
        ['dev', 'Найти простое правило, по которому все начинает работать без лишних действий.'],
        ['infra', 'Навести порядок так, чтобы сбой больше не повторялся и всем было понятно, что делать.'],
        ['creative', 'Передать настроение и смысл через форму, образ, материал или движение.'],
        ['engineering', 'Понять принцип работы системы и заставить разные части согласованно двигаться или реагировать.'],
        ['mechanics', 'Увидеть реальный результат: деталь включилась, двигатель завелся, контакт восстановился.'],
      ],
    },
  ].map(question => ({
    ...question,
    options: question.options.map(([cluster, text]) => ({ cluster, text })),
  }));

  const caseQuestions = {
    dev: {
      title: 'Кейс: сайт лицея',
      scenario: 'На сайте лицея страницы с направлениями открываются медленно. Контент менять нельзя: тексты и карточки программ должны остаться. Нужно понять, как улучшить работу страницы перед приемной кампанией.',
      options: [
        { tag: 'adequate', style: 'systematic', text: 'Сначала проверить, что именно тормозит: изображения, скрипты, лишние запросы или порядок загрузки.' },
        { tag: 'adequate', style: 'pragmatic', text: 'Быстро убрать самые тяжелые элементы из первого экрана и отложить их загрузку после основного контента.' },
        { tag: 'weak', style: 'avoidant', text: 'Сказать, что сайт в целом работает, значит проблема не критичная.' },
        { tag: 'neutral', style: 'research', text: 'Собрать отзывы пользователей, но пока не проверять техническую причину тормозов.' },
      ],
    },
    infra: {
      title: 'Кейс: компьютерный класс',
      scenario: 'В компьютерном классе у части ПК пропадает интернет, а у остальных все работает. До занятия осталось мало времени. Нужно понять, это проблема сети, кабелей, настроек или отдельных компьютеров.',
      options: [
        { tag: 'adequate', style: 'systematic', text: 'Проверить по цепочке: один ПК, кабель, порт, адреса, доступ к локальной сети и выход наружу.' },
        { tag: 'adequate', style: 'pragmatic', text: 'Быстро сравнить рабочий и нерабочий компьютер, чтобы найти отличие в подключении или настройках.' },
        { tag: 'weak', style: 'avoidant', text: 'Пересадить всех за рабочие ПК и не разбираться, почему часть класса выпала.' },
        { tag: 'neutral', style: 'communicative', text: 'Сразу сообщить преподавателю и параллельно собрать, у каких ПК проблема повторяется.' },
      ],
    },
    creative: {
      title: 'Кейс: День открытых дверей',
      scenario: 'Лицей готовит День открытых дверей. Нужен визуал для сайта и постер в холле: он должен быть заметным, но не выглядеть случайным набором ярких элементов.',
      options: [
        { tag: 'adequate', style: 'creative', text: 'Собрать 2-3 визуальные идеи, выбрать одну главную метафору и сделать на ее основе афишу и постер.' },
        { tag: 'adequate', style: 'systematic', text: 'Сначала определить аудиторию, текст, размеры, цвета и только потом собирать макет.' },
        { tag: 'weak', style: 'avoidant', text: 'Взять первый красивый шаблон и заменить текст, не проверяя, подходит ли он лицею.' },
        { tag: 'weak', style: 'chaotic', text: 'Добавить побольше эффектов, чтобы точно было ярко, даже если информация читается хуже.' },
      ],
    },
    engineering: {
      title: 'Кейс: учебный стенд',
      scenario: 'На учебном стенде есть датчики, лампочки и небольшой двигатель. Датчик реагирует, одна лампа загорается, но двигатель не запускается. Нужно понять, где нарушилась работа схемы.',
      options: [
        { tag: 'adequate', style: 'systematic', text: 'Разделить стенд на участки и проверить сигнал от датчика до двигателя по шагам.' },
        { tag: 'adequate', style: 'hands_on', text: 'Проверить питание, контакты, соединения и сам двигатель, чтобы исключить физическую неисправность.' },
        { tag: 'weak', style: 'chaotic', text: 'Сразу менять все соединения подряд, пока что-нибудь случайно не заработает.' },
        { tag: 'neutral', style: 'research', text: 'Посмотреть схему и спросить, как стенд должен работать в нормальном режиме.' },
      ],
    },
    mechanics: {
      title: 'Кейс: учебный автоагрегат',
      scenario: 'На учебном авто двигатель не заводится, а один элемент электрики ведет себя нестабильно. Нужно начать диагностику так, чтобы не пропустить простую причину и не сделать хуже.',
      options: [
        { tag: 'adequate', style: 'systematic', text: 'Проверить питание, предохранители, контакты и признаки неисправности по понятной последовательности.' },
        { tag: 'adequate', style: 'hands_on', text: 'Осмотреть узел, аккуратно проверить соединения и измерить напряжение там, где это безопасно.' },
        { tag: 'weak', style: 'avoidant', text: 'Сразу сказать, что нужен мастер, и не пытаться локализовать проблему.' },
        { tag: 'weak', style: 'chaotic', text: 'Начать разбирать все подряд, чтобы быстрее добраться до причины.' },
      ],
    },
  };

  const realityQuestions = [
    {
      key: 'monotony',
      title: 'Монотонность',
      text: 'Ты записался на курс по выбранному направлению. Каждый день там нужно 2-3 часа делать похожие задания: решать задачи, работать с макетами или настраивать оборудование. Через неделю тебе стало скучно. Что ты чаще всего делаешь?',
      options: [
        { code: 'A', text: 'Понимаю, что это не мое, и прекращаю этим заниматься.', summary: 'можешь быстро выключаться, когда становится однообразно' },
        { code: 'B', text: 'Делаю задания до конца, но без особого удовольствия.', summary: 'можешь доделывать скучные задания, даже если интерес просел' },
        { code: 'C', text: 'Пытаюсь как-то разнообразить задания или добавить что-то свое.', summary: 'ищешь способ оживить однообразную работу' },
        { code: 'D', text: 'Продолжаю, потому что для меня важен результат, даже если скучно.', summary: 'держишься за результат, даже когда процесс становится скучным' },
      ],
    },
    {
      key: 'frustration',
      title: 'Фрустрация',
      text: 'Если у тебя 40-60 минут не получается решить задачу или найти ошибку, ты чаще...',
      options: [
        { code: 'A', text: 'Продолжаю разбираться, меня это даже подзаводит.', summary: 'обычно продолжаешь разбираться, когда задача сопротивляется' },
        { code: 'B', text: 'Делаю перерыв и потом возвращаюсь.', summary: 'умеешь сделать паузу и вернуться к сложной задаче' },
        { code: 'C', text: 'Откладываю и беру другую задачу, иногда так и не возвращаюсь.', summary: 'иногда уходишь в другую задачу и не возвращаешься к первой' },
        { code: 'D', text: 'Бросаю, потому что начинаю злиться или терять интерес.', summary: 'можешь бросить задачу, если долго не получается' },
      ],
    },
  ];

  const styleLabels = {
    systematic: 'системную',
    pragmatic: 'прагматичную',
    creative: 'творческую',
    hands_on: 'практическую',
    communicative: 'коммуникативную',
    research: 'исследовательскую',
    avoidant: 'избегающую',
    chaotic: 'хаотичную',
  };

  const clusterOrder = ['dev', 'infra', 'creative', 'engineering', 'mechanics'];
  const persistenceSensitive = new Set(['dev', 'infra', 'mechanics']);
  const relatedClusters = {
    dev: ['infra', 'creative'],
    infra: ['dev', 'engineering'],
    creative: ['dev', 'engineering'],
    engineering: ['mechanics', 'infra'],
    mechanics: ['engineering', 'infra'],
  };
  const state = {};

  const screens = {
    start: root.querySelector('[data-career-screen="start"]'),
    quiz: root.querySelector('[data-career-screen="quiz"]'),
    result: root.querySelector('[data-career-screen="result"]'),
  };
  const phase = root.querySelector('[data-career-phase]');
  const progress = root.querySelector('[data-career-progress]');
  const progressText = root.querySelector('[data-career-progress-text]');
  const progressPercent = root.querySelector('[data-career-progress-percent]');
  const progressFill = root.querySelector('[data-career-progress-fill]');
  const kicker = root.querySelector('[data-career-kicker]');
  const questionTitle = root.querySelector('[data-career-question]');
  const questionNote = root.querySelector('[data-career-note]');
  const optionsEl = root.querySelector('[data-career-options]');
  const resultEl = root.querySelector('[data-career-result]');

  root.querySelector('[data-career-start]').addEventListener('click', startTest);

  function resetState() {
    state.interestIndex = 0;
    state.caseIndex = 0;
    state.realityIndex = 0;
    state.caseTargets = [];
    state.choices = [];
    state.caseAnswers = {};
    state.realityAnswers = {};
    state.scores = Object.fromEntries(clusterOrder.map(cluster => [cluster, 0]));
  }

  function showScreen(name) {
    Object.values(screens).forEach(screen => screen.classList.remove('active'));
    screens[name].classList.add('active');
  }

  function setProgress(label, done, total) {
    const percent = Math.round((done / total) * 100);
    progress.classList.toggle('hidden', total === 0);
    progress.setAttribute('aria-hidden', total === 0 ? 'true' : 'false');
    progressText.textContent = label;
    progressPercent.textContent = `${percent}%`;
    progressFill.style.width = `${percent}%`;
  }

  function renderOptions(options, handler) {
    optionsEl.innerHTML = '';
    options.forEach(option => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'career-test-option';
      button.textContent = option.text;
      button.addEventListener('click', () => handler(option));
      optionsEl.appendChild(button);
    });
  }

  function startTest() {
    resetState();
    showScreen('quiz');
    renderInterest();
  }

  function totalSteps() {
    return interestQuestions.length + Math.max(state.caseTargets.length, 1) + realityQuestions.length;
  }

  function renderInterest() {
    const question = interestQuestions[state.interestIndex];
    phase.textContent = 'Interest Layer';
    kicker.textContent = 'Вопрос про интересы';
    questionTitle.textContent = question.text;
    questionNote.classList.add('hidden');
    setProgress(`Вопрос ${state.interestIndex + 1} из 8`, state.interestIndex + 1, 12);
    renderOptions(question.options, answerInterest);
  }

  function answerInterest(option) {
    state.scores[option.cluster] += 1;
    state.choices.push(option);
    if (state.interestIndex < interestQuestions.length - 1) {
      state.interestIndex += 1;
      renderInterest();
      return;
    }
    prepareCases();
    renderCase();
  }

  function sortedScores() {
    return clusterOrder
      .map(cluster => [cluster, state.scores[cluster]])
      .sort((a, b) => b[1] - a[1] || clusterOrder.indexOf(a[0]) - clusterOrder.indexOf(b[0]));
  }

  function prepareCases() {
    const sorted = sortedScores();
    const top1 = sorted[0];
    const top2 = sorted[1];
    state.caseTargets = [top1[0]];
    if (top1[1] - top2[1] <= 2) {
      state.caseTargets.push(top2[0]);
    }
    state.caseIndex = 0;
  }

  function renderCase() {
    const cluster = state.caseTargets[state.caseIndex];
    const question = caseQuestions[cluster];
    phase.textContent = 'Case Layer';
    kicker.textContent = question.title;
    questionTitle.textContent = question.scenario;
    questionNote.textContent = 'Выбери стратегию, которая ближе к твоему первому ходу.';
    questionNote.classList.remove('hidden');
    setProgress(`Кейс ${state.caseIndex + 1} из ${state.caseTargets.length}`, 8 + state.caseIndex + 1, totalSteps());
    renderOptions(question.options, option => answerCase(cluster, option));
  }

  function answerCase(cluster, option) {
    state.caseAnswers[cluster] = {
      tag: option.tag,
      style: option.style,
      text: option.text,
    };
    if (state.caseIndex < state.caseTargets.length - 1) {
      state.caseIndex += 1;
      renderCase();
      return;
    }
    state.realityIndex = 0;
    renderReality();
  }

  function renderReality() {
    const question = realityQuestions[state.realityIndex];
    phase.textContent = 'Reality Layer';
    kicker.textContent = question.title;
    questionTitle.textContent = question.text;
    questionNote.classList.add('hidden');
    setProgress(
      `Сценарий ${state.realityIndex + 1} из 2`,
      8 + state.caseTargets.length + state.realityIndex + 1,
      totalSteps(),
    );
    renderOptions(question.options, option => answerReality(question.key, option));
  }

  function answerReality(key, option) {
    state.realityAnswers[key] = option;
    if (state.realityIndex < realityQuestions.length - 1) {
      state.realityIndex += 1;
      renderReality();
      return;
    }
    showResults();
  }

  function interestLevel(score) {
    if (score >= 5) return 'High';
    if (score >= 3) return 'Medium';
    return 'Low';
  }

  function caseLevel(cluster) {
    const answer = state.caseAnswers[cluster];
    if (!answer) return 'Medium';
    if (answer.tag === 'adequate') return 'High';
    if (answer.tag === 'neutral') return 'Medium';
    return 'Low';
  }

  function realityLevel() {
    const monotony = state.realityAnswers.monotony?.code;
    const frustration = state.realityAnswers.frustration?.code;
    if (monotony === 'A' || frustration === 'D') return 'Weak';
    if ((monotony === 'C' || monotony === 'D') && (frustration === 'A' || frustration === 'B')) return 'Strong';
    return 'Medium';
  }

  function canBeMain(cluster, reality) {
    if (interestLevel(state.scores[cluster]) !== 'High') return false;
    if (caseLevel(cluster) !== 'High') return false;
    if (persistenceSensitive.has(cluster) && reality === 'Weak') return false;
    return true;
  }

  function chooseResults(reality) {
    const sorted = sortedScores();
    const mainCandidate = sorted.find(([cluster]) => canBeMain(cluster, reality))
      || sorted.find(([cluster]) => caseLevel(cluster) !== 'Low' && interestLevel(state.scores[cluster]) !== 'Low')
      || sorted[0];
    const main = mainCandidate[0];
    const interestAlternative = sorted.find(([cluster]) => {
      if (cluster === main) return false;
      const scoreGap = sorted[0][1] - state.scores[cluster];
      return scoreGap <= 2 && caseLevel(cluster) !== 'Low' && interestLevel(state.scores[cluster]) !== 'Low';
    });
    const relatedAlternative = relatedClusters[main].find(cluster => cluster !== main);
    const alternative = interestAlternative?.[0] || relatedAlternative;

    return {
      main,
      alternative,
      alternativeSource: interestAlternative ? 'interest' : 'related',
      originalTop: sorted[0][0],
    };
  }

  function realityText(level) {
    const monotony = state.realityAnswers.monotony.summary;
    const frustration = state.realityAnswers.frustration.summary;
    if (level === 'Strong') {
      return `В скучных и сложных задачах ты показал хороший запас устойчивости: ты ${monotony}, а также ${frustration}.`;
    }
    if (level === 'Weak') {
      return `По ответам видно, что однообразие или затяжная ошибка могут быстро сбивать темп: ты ${monotony} и ${frustration}.`;
    }
    return `В рутине ты держишься достаточно ровно: ты ${monotony}, а в сложных моментах ${frustration}.`;
  }

  function whyText(cluster, reality, originalTop, context = 'main') {
    const score = state.scores[cluster];
    const cLevel = caseLevel(cluster);

    if (context === 'related') {
      let text = `Это направление близко к советуемому по типу задач: здесь тоже важно, что ${clusters[cluster].interestText}.`;
      text += ' Оно не спорит с главным результатом, а дает смежную пробу, если хочется проверить соседнюю траекторию.';
      if (persistenceSensitive.has(cluster) && reality === 'Weak') {
        text += ' В нем много повторов и поиска ошибок, поэтому лучше начинать с маленькой практической задачи.';
      }
      return text;
    }

    let text = `У тебя ${score} из 8 по интересу: в ситуациях ты чаще выбирал задачи, где ${clusters[cluster].interestText}.`;
    if (cLevel === 'High') {
      text += ' В кейсе ты выбрал рабочую стратегию, поэтому направление выглядит не только интересным, но и практически близким.';
    } else if (cLevel === 'Low') {
      text += ' При этом в кейсе есть рассинхрон: интерес есть, но выбранная стратегия пока мало похожа на подход специалистов в этой сфере.';
    } else {
      text += ' Поведенческий сигнал умеренный: направление стоит попробовать небольшой задачей, чтобы проверить ощущение на практике.';
    }
    if (persistenceSensitive.has(cluster) && reality === 'Weak') {
      text += ' В этом направлении много повторов и поиска ошибок, поэтому важно заранее тренировать терпение к рутине.';
    }
    if (cluster !== originalTop) {
      text += ' Итог учитывает не только интерес, но и кейс, поэтому рекомендация могла сместиться от первого интереса.';
    }
    return text;
  }

  function howList(cluster, reality) {
    const caseAnswer = state.caseAnswers[cluster];
    const caseLine = caseAnswer
      ? `В кейсе про ${clusters[cluster].caseName} ты выбрал ${styleLabels[caseAnswer.style]} стратегию: это похоже на реальную работу в направлении.`
      : 'По этому направлению кейс не показывался, поэтому оно идет как предполагаемая альтернатива на основе интересов.';
    return [
      `В вопросах про ситуации ты чаще выбирал варианты, где ${clusters[cluster].interestText}.`,
      caseLine,
      realityText(reality),
    ];
  }

  function renderResultBlock(cluster, reality, originalTop, alternative = false, alternativeSource = 'interest') {
    const data = clusters[cluster];
    const warning = reality === 'Weak'
      ? '<p class="career-test-warning">Важно: скука или затяжные ошибки могут мешать старту. Это не запрет, но хороший повод пробовать направление маленькими задачами.</p>'
      : '';
    const how = howList(cluster, reality).map(item => `<li>${item}</li>`).join('');
    const realityItems = data.reality.map(item => `<li>${item}</li>`).join('');

    if (alternative) {
      const context = alternativeSource === 'related' ? 'related' : 'alternative';
      return `
        <div class="career-test-result-card wide alt">
          <h3>Предполагаемое направление для пробы</h3>
          <p><strong>${data.title}</strong>: ${data.programs.join(', ')}.</p>
          <p>${whyText(cluster, reality, originalTop, context)}</p>
          <p><strong>Мини-задача на 10 минут:</strong> ${data.tenMinutes}</p>
        </div>
      `;
    }

    return `
      <div class="career-test-result-hero">
        <span class="career-test-result-label">Советуемое направление</span>
        <h2 class="career-test-result-title">${data.title}</h2>
        <p class="career-test-programs">${data.programs.join(' | ')}</p>
      </div>
      <div class="career-test-result-grid">
        <div class="career-test-result-card wide">
          <h3>Почему</h3>
          <p>${whyText(cluster, reality, originalTop, 'main')}</p>
          ${warning}
        </div>
        <div class="career-test-result-card">
          <h3>Как ты это показал</h3>
          <ul>${how}</ul>
        </div>
        <div class="career-test-result-card">
          <h3>Реальность работы</h3>
          <ul>${realityItems}</ul>
        </div>
        <div class="career-test-result-card wide">
          <h3>Что сделать за 10 минут</h3>
          <p>${data.tenMinutes}</p>
        </div>
      </div>
    `;
  }

  function showResults() {
    const reality = realityLevel();
    const decision = chooseResults(reality);
    const desync = Object.keys(state.caseAnswers)
      .filter(cluster => interestLevel(state.scores[cluster]) === 'High' && caseLevel(cluster) === 'Low')
      .filter(cluster => cluster !== decision.main);

    let html = renderResultBlock(decision.main, reality, decision.originalTop);
    html += renderResultBlock(
      decision.alternative,
      reality,
      decision.originalTop,
      true,
      decision.alternativeSource,
    );

    if (desync.length) {
      html += `
        <div class="career-test-result-card wide">
          <h3>Замечание по рассинхрону</h3>
          <p>Тебе интересно направление ${desync.map(cluster => clusters[cluster].title).join(', ')}, но по кейсу видно, что стиль решения пока расходится с типичным подходом. Его можно пробовать, но лучше не делать единственным выбором прямо сейчас.</p>
        </div>
      `;
    }

    html += `
      <div class="career-test-actions">
        <a class="btn btn-gold" href="#directions-section">Посмотреть направления</a>
        <button class="btn btn-secondary" type="button" data-career-restart>Пройти еще раз</button>
      </div>
    `;

    resultEl.innerHTML = html;
    resultEl.querySelector('[data-career-restart]').addEventListener('click', startTest);
    phase.textContent = 'Результат';
    setProgress('Готово', totalSteps(), totalSteps());
    showScreen('result');
  }

  resetState();
});
