document.addEventListener('DOMContentLoaded', function () {
	const button = document.getElementById('quote-button');
	const authorInfoSection = document.getElementById('author-info');
	const personName = document.getElementById('person-name');
	const personInfo = document.getElementById('person-info');

	button.addEventListener('click', async function () {
		 const person = button.getAttribute('data-person');
		 personName.textContent = "Загрузка...";
		 personInfo.textContent = "";
		 authorInfoSection.classList.remove('hide');
		 authorInfoSection.classList.add('show');

		 try {
			  const info = await fetchPersonInfo(person);
			  const translatedInfo = await translateText(info, 'ru');
			  personName.textContent = person.replace('_', ' ');
			  personInfo.textContent = translatedInfo;
		 } catch (error) {
			  personName.textContent = "Ошибка";
			  personInfo.textContent = "Не удалось загрузить информацию.";
		 }
	});

	async function fetchPersonInfo(person) {
		 const response = await fetch(`https://en.wikipedia.org/api/rest_v1/page/summary/${person}`);
		 if (!response.ok) {
			  throw new Error('Network response was not ok');
		 }
		 const data = await response.json();
		 return data.extract;
	}

	async function translateText(text, targetLang) {
		 const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${targetLang}&dt=t&q=${encodeURIComponent(text)}`;
		 const response = await fetch(url);
		 if (!response.ok) {
			  throw new Error('Translation network response was not ok');
		 }
		 const data = await response.json();
		 return data[0][0][0];
	}
});
