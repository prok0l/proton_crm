document.addEventListener('DOMContentLoaded', () => {

  const mask = (dataValue, options) => { // создаем универсальную функцию
    const elements = document.querySelectorAll(`[data-mask="${dataValue}"]`) // ищем поля ввода по селектору с переданным значением data-атрибута
    if (!elements) return // если таких полей ввода нет, прерываем функцию

    elements.forEach(el => { // для каждого из полей ввода
      IMask(el, options) // инициализируем плагин imask для необходимых полей ввода с переданными параметрами маски
    })
  }

  // Используем наше функцию mask для разных типов масок

  // Маска для номера телефона
  mask('phone', {
    mask: '+{7}(000)000-00-00'
  })

  // Маска для почтового индекса
  mask('postalCode', {
    mask: '000000' // шесть цифр
  })

  // Маска для даты
  mask('date', {
    mask: Date,
    min: new Date(1900, 0, 1), // минимальная дата 01.01.1900
  })

  // Маска для числа
  mask('number', {
    mask: Number,
    thousandsSeparator: ' ' // разделитель тысяч в числе
  })

})
