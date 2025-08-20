![](./assets/GOO-D-Inicio.gif)

<br>

<h1 align="center">🍳 GOO:D 🍽️</h1>

<div align="center">

![Django](https://img.shields.io/badge/Django-green)
![Python](https://img.shields.io/badge/Python-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-yellow)
![MySQL](https://img.shields.io/badge/MySQL-lightblue)
![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red)
![Deployed on Alwaysdata](https://img.shields.io/badge/Deployed%20on-Alwaysdata-violet)

</div>

---

### 🇪🇸 Español

🎉 **GOO:D** es más que un recetario; es tu compañero para crear, descubrir y compartir platos con pasión y facilidad.  
Animado y cuidadosamente diseñado, combina lo mejor de **Django**, **JavaScript**, **SASS** y librerías modernas como **Quill** y **Select2** para ofrecer una experiencia culinaria única.  

*God! Good! Go!* — Un recetario multilingüe que combina inspiración, calidad y acción para amantes de la cocina.  

Además, GOO:D significa también **Comparte Disfruta Sonríe :D** — porque cocinar es todo eso.


### 🇬🇧 English

🎉 **GOO:D** is more than just a cookbook; it’s your companion to create, discover, and share dishes with passion and ease.  
Playful yet carefully crafted, it blends the power of **Django**, **JavaScript**, **SASS**, and modern libraries like **Quill** and **Select2** to deliver a unique culinary experience.  

*God! Good! Go!* — A multilingual recipe book that brings together inspiration, quality, and action for food lovers.  

And GOO:D also means **Share Enjoy Smile :D** — because cooking is all of that.


<br>

---

## 📸 Capturas de pantalla  
### Screenshots | Schermate | Captures | Képernyőképek | Capturas

<details>
<summary>🔹Inicio / Home 🔹 Recetas / Recipes 🔹 Detalle receta / Recipe page🔹</summary>

  <br>

| Inicio / Home | Recetas / Recipes | Detalle receta / Recipe page |
|---------------|------------------|-------------------|
| ![Inicio](./assets/GOO-D-Inicio.jpg) | ![Recetas](./assets/pagina-recetas.jpg) | ![Detalle](./assets/detalle-receta.png)|

</details>

<details>
<summary>🔸Buscador / Search 🔸 Perfil (datos / data) 🔸 Perfil (recetas / recipes)🔸</summary>

  <br>

| Buscador / Search | Perfil / Profile (datos / data) | Perfil / Profile (recetas /recipes) |
|------------------------------|--------------------------|----------------------------|
| ![Buscador](./assets/buscar-recetas.png)  | ![Perfil datos](./assets/perfil-datos-usuario.png) | ![Perfil recetas](./assets/perfil-recetas.png) |

</details>

<details>
<summary>🔺Perfil (favoritas / favorites) 🔺 Comentarios / Comments 🔺 Puntuaciones / Rating🔺</summary>

  <br>

| Perfil / Profile (favoritas / favorites) | Perfil / Profile (comentarios / comments) | Perfil / Profile (puntuaciones / rating) |
|------------------------------|-------------------------------|---------------------------------|
| ![Favoritas](./assets/perfil-favoritas.png) | ![Comentarios](./assets/perfil-comentarios.png) | ![Puntuaciones](./assets/perfil-puntuaciones.png) |

</details>

  <br>

## 🎥 Demo en vídeo
### Demo video | Demo in video | Demostració en vídeo | Videó bemutató | Demonstração em vídeo

| 🏠 Home | 📋 Recipes | 📖 Recipe page | ✏️ Create / Update form |
|---------|------------|----------------|-------------------------|
| [![Home](./assets/thumb-home.png)](./assets/GOO-D-Inicio1.mp4) | [![Recipes](./assets/thumb-recipes.png)](./assets/recipes-list.mp4) | [![Recipe](./assets/thumb-recipe.png)](./assets/recipe-page.mp4) | [![Form](./assets/thumb-form.png)](./assets/create-update-form.mp4) |

---
<br>

<details>
<summary>🇪🇸 Español</summary>

## 🍽️ ¿Qué es GOO:D?

**GOO:D** es una plataforma web para compartir recetas, con soporte multilingüe, diseño responsivo y animaciones cuidadas. Está pensada para usuarios anónimos y registrados, ofreciendo una experiencia rica, visual y funcional.

<br>

### 🚀 Tecnologías usadas

- **Backend:** Django
- **Frontend:** JavaScript, SASS, AJAX
- **Interfaces ricas:** Quill, Select2 (TinyMCE para administración)
- **Traducción automática:** `LibreTranslate` 

<br>

### 👥 Funcionalidades por tipo de usuario

| Funcionalidad                                       | Visitantes (sin login) 👫 | Usuarios registrados 🔐 |
|-----------------------------------------------------|---------------------------|--------------------------|
| Ver recetas                                        | ✅                        | ✅                       |
| Búsqueda avanzada con filtros                      | ✅                        | ✅                       |
| Sliders temáticos de recetas                       | ✅                        | ✅                       |
| Sección sorpresa ("¿No sabes qué cocinar?")        | ✅                        | ✅                       |
| Guardar recetas favoritas                          | ❌                        | ✅                       |
| Comentar recetas                                   | ❌                        | ✅                       |
| Puntuar recetas                                    | ❌                        | ✅                       |
| Perfil con avatar y datos                          | ❌                        | ✅                       |
| Subir recetas (convertirse en autor)               | ❌                        | ✅                       |
| Editar / borrar recetas propias                    | ❌                        | ✅ (solo autores)        |

<br>

### 🛠️ Administración
- Panel de Django Admin completo.
- Gestión de usuarios, recetas, ingredientes, categorías y más.
- Solo accesible para superusuarios.

<br>

### 🌍 Traducciones automáticas

- Las recetas creadas en un idioma se traducen automáticamente al resto de idiomas disponibles.  
- Para los textos de la interfaz se utiliza **Django i18n**, con soporte de **Rosetta** y **Parler**.  
- Para los campos de texto libre, las traducciones se generan mediante **LibreTranslate** en producción.
- Además, se han realizado más de 2600 traducciones manuales para garantizar calidad y naturalidad en los idiomas soportados.

<br>

### 🧾 Formularios detallados

Los formularios de creación/edición de recetas permiten:

- Agregar ingredientes organizados
- Redactar pasos detallados
- Elegir múltiples categorías
- Asignar tags, alérgenos, dificultad, tipo de comida, tiempo, etc.
- Tooltips en labels para guía

<br>

### 🎨 Interfaz y diseño
| 🧩 **Bloque**                      | 📋 **Contenido**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🌐 General                         | • Responsive (mobile-first)<br>• Animaciones y microinteracciones cuidadas<br>• Navegación creativa:<br>  🔄 Logo: plato giratorio con mantel al hover/click<br>  🍴 Utensilios como enlaces, mesa puesta como menú                                                                                                                                                                                                                                                                                                             |
| 📑 Página de lista de recetas      | • Top recetas: según puntuación media ⭐<br>• Recientes: por fecha de publicación 🕒<br>• Favoritas: las más guardadas 💖<br>• Fáciles: nivel de dificultad "fácil" 🥄<br>• Recetas de la cocina "xyz" (dinámico): del tipo de cocina con más recetas subidas 🍲<br>• Recetas de actualidad (dinámico): se activan y muestran las recetas según temática 🎉 (temporadas, estaciones, festividades: Halloween 🎃, Navidad 🎄, Nochevieja 🎆, San Valentín 💘, Carnaval 🎭, Día del Padre 👨, Día de la Madre 👩, Pascua 🐣, etc.) |
| 👤 Sección especial de "Mi perfil" | • Diseño único ✨<br>• Secciones varias:<br>  📝 Datos personales: datos de usuario, cambios de avatar, email o contraseña<br>  📤 Recetas subidas propias<br>  💾 Favoritas: las recetas marcadas como favoritas y guardadas en esta sección<br>  💬 Comentarios:<br>    – "mis comentarios"<br>    – "respuestas a mis comentarios"<br>    – "comentarios en mis recetas"<br>  ⭐ Mis puntuaciones: lista de recetas valoradas por el usuario                                                                                   |


### 📧 Extras

- Formulario de contacto con sistema de correos
- Funcionalidad completa de login, registro y recuperación de contraseña vía email

<br>

> **Nota:** Este proyecto se ha creado con fines demostrativos para evaluación académica.  
> Los textos e imágenes de las recetas provienen de [Comedera](https://comedera.com) y son propiedad de sus autores.

<br>

## 🚀 Despliegue

El backend está desplegado en **Alwaysdata**, integrado con el frontend y con soporte multilenguaje.  
La traducción automática se realiza mediante una API externa en producción.

👉 Puedes acceder a la aplicación en:  
[https://goodgo.alwaysdata.net/](https://goodgo.alwaysdata.net/)

<br>

## 📫 Contacto

[![Email](https://img.shields.io/badge/Email-red?logo=gmail&logoColor=white)](mailto:sanyimo@gmail.com)  
[![GitHub](https://img.shields.io/badge/GitHub-black?logo=github)](https://github.com/sanyimo)  
[![Discord](https://img.shields.io/badge/Discord-blue?logo=discord)](https://discordapp.com/users/1300827475424837685)  

---

<br>

</details>

<details>
<summary>🇬🇧 English</summary>

## 🍽️ What is GOO:D?

**GOO:D** is a web platform for sharing recipes, with multilingual support, responsive design, and smooth animations. It’s designed for both anonymous and registered users, offering a rich, visual, and functional experience.

<br>

### 🚀 Technologies used

- **Backend:** Django  
- **Frontend:** JavaScript, SASS, AJAX  
- **Rich interfaces:** Quill, Select2 (TinyMCE for administration)  
- **Automatic translation:** `LibreTranslate`   

<br>

### 👥 Features by user type

| Feature                                             | Visitors (no login) 👫 | Registered users 🔐 |
|-----------------------------------------------------|-------------------------|----------------------|
| View recipes                                        | ✅                      | ✅                   |
| Advanced search with filters                        | ✅                      | ✅                   |
| Thematic recipe sliders                             | ✅                      | ✅                   |
| Surprise section ("Don’t know what to cook?")       | ✅                      | ✅                   |
| Save favorite recipes                               | ❌                      | ✅                   |
| Comment on recipes                                  | ❌                      | ✅                   |
| Rate recipes                                        | ❌                      | ✅                   |
| Profile with avatar and data                        | ❌                      | ✅                   |
| Upload recipes (become an author)                   | ❌                      | ✅                   |
| Edit / delete own recipes                           | ❌                      | ✅ (authors only)    |

<br>

### 🛠️ Administration
- Full Django Admin panel  
- Management of users, recipes, ingredients, categories, and more  
- Accessible only to superusers  

<br>

### 🌍 Automatic translations

- Recipes created in one language are automatically translated into all the other available languages.  
- Interface texts are managed with **Django i18n**, supported by **Rosetta** and **Parler**.  
- Free-text fields are translated using **LibreTranslate** in production.
- In addition, over 2600 manual translations have been done to ensure quality and naturalness in all supported languages.

<br>

### 🧾 Detailed forms

The recipe creation/editing forms allow:  

- Adding organized ingredients  
- Writing detailed steps  
- Choosing multiple categories  
- Assigning tags, allergens, difficulty, meal type, time, etc.  
- Labels with tooltips as a guide  

<br>

### 🎨 Interface and design

| 🧩 **Block**                    | 📋 **Content**                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🌐 General                      | • Responsive (mobile-first)<br>• Carefully crafted animations and micro-interactions<br>• Creative navigation:<br>  🔄 Logo: spinning plate with animated tablecloth on hover/click<br>  🍴 Utensils as links, table set as menu                                                                                                                                                                                                                                        |
| 📑 Recipe list page             | • Top recipes: by average rating ⭐<br>• Recent: by publication date 🕒<br>• Favorites: most saved 💖<br>• Easy: “easy” difficulty recipes 🥄<br>• Cuisine “xyz” (dynamic): cuisine type with most uploaded recipes 🍲<br>• Seasonal recipes (dynamic): activated and shown depending on theme 🎉 (seasons, holidays, special events: Halloween 🎃, Christmas 🎄, New Year’s Eve 🎆, Valentine’s Day 💘, Carnival 🎭, Father’s Day 👨, Mother’s Day 👩, Easter 🐣, etc.) |
| 👤 Special “My profile” section | • Unique design ✨<br>• Several areas:<br>  📝 Personal data: user info, avatar, email or password changes<br>  📤 Own uploaded recipes<br>  💾 Favorites: recipes marked as favorites and saved in this section<br>  💬 Comments:<br>    – “my comments”<br>    – “replies to my comments”<br>    – “comments on my recipes”<br>  ⭐ My ratings: list of recipes rated by the user                                                                                       |


<br>

### 📧 Extras

- Contact form with email system 
- Full login, registration, and password recovery via email  

> **Note:** This project was created for academic evaluation purposes.  
> The recipe texts and images come from [Comedera](https://comedera.com) and are the property of their authors.  

<br>

## 🚀 Deployment

The backend is deployed on **Alwaysdata**, integrated with the frontend and with multilanguage support.  
Automatic translation is handled by an external API in production.  

Access the app at:  
[https://goodgo.alwaysdata.net/](https://goodgo.alwaysdata.net/)

<br>

## 📫 Contact

[![Email](https://img.shields.io/badge/Email-red?logo=gmail&logoColor=white)](mailto:sanyimo@gmail.com)  
[![GitHub](https://img.shields.io/badge/GitHub-black?logo=github)](https://github.com/sanyimo)  
[![Discord](https://img.shields.io/badge/Discord-blue?logo=discord)](https://discordapp.com/users/1300827475424837685)  

---
<br>

</details>

<details>
<summary>🇨🇦 Català</summary>

## 🍽️ Què és GOO:D?

**GOO:D** és una plataforma web per compartir receptes, amb suport multilingüe, disseny responsive i animacions suaus. Està pensada tant per a usuaris anònims com registrats, oferint una experiència rica, visual i funcional.  

<br>

### 🚀 Tecnologies utilitzades

- **Backend:** Django  
- **Frontend:** JavaScript, SASS, AJAX  
- **Interfícies riques:** Quill, Select2 (TinyMCE per a l’administració)  
- **Traducció automàtica:** `LibreTranslate`  

<br>

### 👥 Funcionalitats segons tipus d’usuari  

| Funcionalitat                                        | Visitants (sense login) 👫 | Usuaris registrats 🔐 |
|------------------------------------------------------|----------------------------|------------------------|
| Veure receptes                                       | ✅                         | ✅                     |
| Cerca avançada amb filtres                           | ✅                         | ✅                     |
| Sliders temàtics de receptes                         | ✅                         | ✅                     |
| Secció sorpresa ("No saps què cuinar?")              | ✅                         | ✅                     |
| Guardar receptes preferides                          | ❌                         | ✅                     |
| Comentar receptes                                    | ❌                         | ✅                     |
| Valorar receptes                                     | ❌                         | ✅                     |
| Perfil amb avatar i dades                            | ❌                         | ✅                     |
| Pujar receptes (esdevenir autor)                     | ❌                         | ✅                     |
| Editar / eliminar receptes pròpies                   | ❌                         | ✅ (només autors)      |  

<br>

### 🛠️ Administració  
- Panell complet de Django Admin.  
- Gestió d’usuaris, receptes, ingredients, categories i més.  
- Només accessible per a superusuaris.  

<br>

### 🌍 Traduccions automàtiques

- Les receptes creades en un idioma es tradueixen automàticament a la resta d’idiomes disponibles.
- Per als textos de la interfície s’utilitza Django i18n, amb suport de Rosetta i Parler.
- Per als camps de text lliure, les traduccions es generen amb LibreTranslate en producció.
- A més, s’han realitzat més de 2600 traduccions manuals per garantir qualitat i naturalitat en els idiomes disponibles.

<br>

### 🧾 Formularis detallats  

Els formularis de creació/edició de receptes permeten:  

- Afegir ingredients organitzats  
- Escriure passos detallats  
- Escollir múltiples categories  
- Assignar etiquetes, al·lèrgens, dificultat, tipus d’àpat, temps, etc.  
- Etiquetes amb tooltips com a guia  

<br>

### 🎨 Interfície i disseny  

| 🧩 **Bloc**                        | 📋 **Contingut**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🌐 General                         | • Responsive (mobile-first)<br>• Animacions i microinteraccions cuidades ✨<br>• Navegació creativa:<br>  🔄 Logo: plat giratori amb estovalla animada en hover/click<br>  🍴 Estris com a enllaços, taula parada com a menú                                                                                                                                                                                                                                                                                           |
| 📑 Pàgina de receptes              | • Receptes top: per mitjana de valoracions ⭐<br>• Recents: per data de publicació 🕒<br>• Preferides: més guardades 💖<br>• Fàcils: receptes amb dificultat “fàcil” 🥄<br>• Receptes de la Cuina “xyz” (dinàmica): tipus de cuina amb més receptes pujades 🍲<br>• Receptes d’actualitat (dinàmica): activades i mostrades segons temàtica 🎉 (estacions, festes, esdeveniments especials: Halloween 🎃, Nadal 🎄, Cap d’Any 🎆, Sant Valentí 💘, Carnestoltes 🎭, Dia del Pare 👨, Dia de la Mare 👩, Pasqua 🐣, etc.) |
| 👤 Secció especial “El meu perfil” | • Disseny únic ✨<br>• Diverses àrees:<br>  📝 Dades personals: informació d’usuari, canvi d’avatar, email o contrasenya<br>  📤 Receptes pròpies pujades<br>  💾 Favorites: receptes marcades i guardades en aquesta secció<br>  💬 Comentaris:<br>    – “els meus comentaris”<br>    – “respostes als meus comentaris”<br>    – “comentaris a les meves receptes”<br>  ⭐ Les meves valoracions: llista de receptes valorades per l’usuari                                                                              |


<br>

### 📧 Extres  

- Formulari de contacte amb sistema d’email
- Sistema complet de login, registre i recuperació de contrasenya per email  

> **Nota:** Aquest projecte s’ha creat amb finalitats d’avaluació acadèmica.  
> Els textos i imatges de les receptes provenen de [Comedera](https://comedera.com) i són propietat dels seus autors.  

<br>

## 🚀 Desplegament  

El backend està desplegat a **Alwaysdata**, integrat amb el frontend i amb suport multillenguatge.  
La traducció automàtica es realitza mitjançant una API externa en producció.   

👉 Accés a l’aplicació en:  
[https://goodgo.alwaysdata.net/](https://goodgo.alwaysdata.net/)

<br>

## 📫 Contacte  

[![Email](https://img.shields.io/badge/Email-red?logo=gmail&logoColor=white)](mailto:sanyimo@gmail.com)  
[![GitHub](https://img.shields.io/badge/GitHub-black?logo=github)](https://github.com/sanyimo)  
[![Discord](https://img.shields.io/badge/Discord-blue?logo=discord)](https://discordapp.com/users/1300827475424837685)  

---

<br>

</details>

<details>
<summary>🇮🇹 Italiano</summary>

## 🍽️ Che cos’è GOO:D?

**GOO:D** è una piattaforma web per condividere ricette, con supporto multilingue, design responsive e animazioni fluide. È pensata sia per utenti anonimi sia registrati, offrendo un’esperienza ricca, visiva e funzionale.  

<br>

### 🚀 Tecnologie utilizzate

- **Backend:** Django  
- **Frontend:** JavaScript, SASS, AJAX  
- **Interfacce ricche:** Quill, Select2 (TinyMCE per l’amministrazione)  
- **Traduzione automatica:** `LibreTranslate`

<br>

### 👥 Funzionalità per tipo di utente  

| Funzionalità                                         | Visitatori (senza login) 👫 | Utenti registrati 🔐 |
|------------------------------------------------------|-----------------------------|-----------------------|
| Visualizzare ricette                                 | ✅                          | ✅                    |
| Ricerca avanzata con filtri                          | ✅                          | ✅                    |
| Slider tematici di ricette                           | ✅                          | ✅                    |
| Sezione sorpresa ("Non sai cosa cucinare?")          | ✅                          | ✅                    |
| Salvare ricette preferite                            | ❌                          | ✅                    |
| Commentare ricette                                   | ❌                          | ✅                    |
| Valutare ricette                                     | ❌                          | ✅                    |
| Profilo con avatar e dati                            | ❌                          | ✅                    |
| Caricare ricette (diventare autore)                  | ❌                          | ✅                    |
| Modificare / eliminare le proprie ricette            | ❌                          | ✅ (solo autori)      |  

<br>

### 🛠️ Amministrazione  
- Pannello completo di Django Admin  
- Gestione di utenti, ricette, ingredienti, categorie e altro  
- Accesso riservato ai superuser  

<br>

### 🌍 Traduzioni automatiche

- Le ricette create in una lingua vengono tradotte automaticamente nelle altre lingue disponibili.  
- Per i testi dell’interfaccia viene utilizzato Django i18n, con il supporto di Rosetta e Parler.
- Per i campi di testo libero, le traduzioni vengono generate con LibreTranslate in produzione.
- Inoltre, sono state effettuate oltre 2600 traduzioni manuali per garantire qualità e naturalezza nelle lingue supportate.

<br>

### 🧾 Form dettagliati  

I form di creazione/modifica delle ricette permettono di:  

- Aggiungere ingredienti organizzati  
- Scrivere passaggi dettagliati  
- Selezionare più categorie  
- Assegnare tag, allergeni, difficoltà, tipo di pasto, tempo, ecc.  
- Tag con tooltip come guida  

<br>

### 🎨 Interfaccia e design  

| 🧩 **Blocco**                        | 📋 **Contenuto**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🌐 Generale                          | • Responsive (mobile-first)<br>• Animazioni e microinterazioni curate ✨<br>• Navigazione creativa:<br>  🔄 Logo: piatto rotante con tovaglia animata su hover/click<br>  🍴 Utensili come link, tavola apparecchiata come menù                                                                                                                                                                                                                                                                                   |
| 📑 Pagina ricette                    | • Ricette top: per media delle valutazioni ⭐<br>• Recenti: per data di pubblicazione 🕒<br>• Preferite: più salvate 💖<br>• Facili: ricette con difficoltà “facile” 🥄<br>• Ricette dalla cucina “xyz” (dinamica): tipo di cucina con più ricette caricate 🍲<br>• Ricette stagionali (dinamiche): attivate e mostrate in base al periodo 🎉 (stagioni, feste, eventi speciali: Halloween 🎃, Natale 🎄, Capodanno 🎆, San Valentino 💘, Carnevale 🎭, Festa della mamma 👩, Festa del papà 👨, Pasqua 🐣, ecc.) |
| 👤 Sezione speciale “Il mio profilo” | • Design personalizzato ✨<br>• Diverse aree:<br>  📝 Dati personali: info utente, cambio avatar, email o password<br>  📤 Ricette proprie caricate<br>  💾 Preferite: ricette contrassegnate e salvate in questa sezione<br>  💬 Commenti:<br>    – “i miei commenti”<br>    – “risposte ai miei commenti”<br>    – “commenti alle mie ricette”<br>  ⭐ Le mie valutazioni: elenco delle ricette valutate dall’utente                                                                                             |

<br>

### 📧 Extra  

- Form di contatto con sistema email  
- Sistema completo di login, registrazione e recupero password via email  

> **Nota:** Questo progetto è stato creato per finalità di valutazione accademica.  
> I testi e le immagini delle ricette provengono da [Comedera](https://comedera.com) e sono di proprietà dei rispettivi autori.  

<br>

## 🚀 Deployment  

Il backend è distribuito su **Alwaysdata**, integrato con il frontend e con supporto multilingue.  
La traduzione automatica è gestita da un'API esterna in produzione.    

👉 Accesso all’applicazione:  
[https://goodgo.alwaysdata.net/](https://goodgo.alwaysdata.net/)

<br>

## 📫 Contatti  

[![Email](https://img.shields.io/badge/Email-red?logo=gmail&logoColor=white)](mailto:sanyimo@gmail.com)  
[![GitHub](https://img.shields.io/badge/GitHub-black?logo=github)](https://github.com/sanyimo)  
[![Discord](https://img.shields.io/badge/Discord-blue?logo=discord)](https://discordapp.com/users/1300827475424837685)  

---

<br>

</details>

<details>
<summary>🇭🇺 Magyar</summary>

## 🍽️ Mi az a GOO:D?

A **GOO:D** egy webes receptmegosztó platform, többnyelvű támogatással, reszponzív dizájnnal és gördülékeny animációkkal. Úgy lett kialakítva, hogy anonim és regisztrált felhasználóknak egyaránt gazdag, vizuális és funkcionális élményt nyújtson.  

<br>

### 🚀 Használt technológiák

- **Backend:** Django  
- **Frontend:** JavaScript, SASS, AJAX  
- **Gazdag felületek:** Quill, Select2 (TinyMCE admin felülethez)  
- **Automatikus fordítás:** `LibreTranslate` használatával

<br>

### 👥 Jellemzők felhasználói típus szerint

| Funkció                                              | Látogatók (bejelentkezés nélkül) 👫 | Regisztrált felhasználók 🔐 |
|------------------------------------------------------|-------------------------------------|-----------------------------|
| Receptek megtekintése                                | ✅                                  | ✅                          |
| Részletes keresés szűrőkkel                          | ✅                                  | ✅                          |
| Tematikus recept-slider                              | ✅                                  | ✅                          |
| Meglepetés szekció ("Nem tudod, mit főzz?")          | ✅                                  | ✅                          |
| Kedvencek mentése                                    | ❌                                  | ✅                          |
| Receptek kommentálása                                | ❌                                  | ✅                          |
| Receptek értékelése                                  | ❌                                  | ✅                          |
| Profil avatarral és adatokkal                        | ❌                                  | ✅                          |
| Receptek feltöltése (szerzővé válás)                 | ❌                                  | ✅                          |
| Saját receptek szerkesztése / törlése                | ❌                                  | ✅ (csak a szerző)          |  

<br>

### 🛠️ Adminisztráció  
- Teljes Django Admin felület  
- Felhasználók, receptek, hozzávalók, kategóriák stb. kezelése  
- Hozzáférés csak szuperusereknek  

<br>


### 🌍 Automatikus fordítások

- Az egyik nyelven létrehozott receptek automatikusan lefordításra kerülnek a többi elérhető nyelvre.  
- A felület szövegei **Django i18n** segítségével vannak kezelve, **Rosetta** és **Parler** támogatással.  
- A szabad szöveges mezők setében a fordításokat LibreTranslate segítségével készítjük élőben.
- Ezen felül több mint 2600 kézi fordítás készült a minőség és a természetesség biztosítása érdekében az összes támogatott nyelven.

<br>


### 🧾 Részletes űrlapok  

A recept létrehozó/szerkesztő űrlap lehetővé teszi:  

- Hozzávalók strukturált hozzáadását  
- Lépésről lépésre történő leírást  
- Több kategória kiválasztását  
- Címkék, allergének, nehézségi szint, ételtípus, elkészítési idő stb. beállítását  
- Tooltip-es címkék használatát útmutatóként  

<br>

### 🎨 Felület és dizájn  

| 🧩 **Blokk**                    | 📋 **Tartalom**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🌐 Általános                    | • Reszponzív (mobile-first)<br>• Gondosan megtervezett animációk és mikrointerakciók ✨<br>• Kreatív navigáció:<br>  🔄 Logó: forgó tányér animált terítővel hover/kattintásra<br>  🍴 Eszközök mint linkek, megterített asztal mint menü                                                                                                                                                                                                                                                                |
| 📑 Receptek oldala              | • Top receptek: értékelési átlag alapján ⭐<br>• Legújabbak: feltöltési dátum szerint 🕒<br>• Kedvencek: legtöbbször elmentett receptek 💖<br>• Könnyű: “könnyű” nehézségű receptek 🥄<br>• “xyz” konyha receptjei (dinamikus): a legtöbb receptet tartalmazó konyhatípus 🍲<br>• Szezonális receptek (dinamikus): időszakhoz igazodó receptek 🎉 (évszakok, ünnepek, események: Halloween 🎃, Karácsony 🎄, Szilveszter 🎆, Valentin-nap 💘, Farsang 🎭, Anyák napja 👩, Apák napja 👨, Húsvét 🐣 stb.) |
| 👤 Speciális “Profilom” szekció | • Testreszabott dizájn ✨<br>• Több rész:<br>  📝 Személyes adatok: felhasználói információk, avatar, email és jelszó módosítása<br>  📤 Saját feltöltött receptek<br>  💾 Kedvencek: a kedvencként megjelölt és elmentett receptek ebben a szakaszban<br>  💬 Kommentek:<br>    – “saját kommentjeim”<br>    – “válaszok a kommentjeimre”<br>    – “kommentek a receptjeimhez”<br>  ⭐ Saját értékelések: a felhasználó által értékelt receptek listája                                                  |

<br>

### 📧 Extrák  

- Kapcsolatfelvételi űrlap email küldéssel
- Teljes bejelentkezési, regisztrációs és jelszó-helyreállító rendszer emailen keresztül  

> **Megjegyzés:** Ez a projekt oktatási célból készült.  
> A receptek szövegei és képei a [Comedera](https://comedera.com) oldalról származnak, és a szerzők tulajdonát képezik.  

<br>

## 🚀 Telepítés  

A backend, frontenddel integrálva, az **Alwaysdata**-ra van telepítve, és többnyelvű támogatású.  
Az automatikus fordítást egy külső API kezeli élőben.   

👉 Alkalmazás elérése itt:  
[https://goodgo.alwaysdata.net/](https://goodgo.alwaysdata.net/)

<br>

## 📫 Kapcsolat  

[![Email](https://img.shields.io/badge/Email-red?logo=gmail&logoColor=white)](mailto:sanyimo@gmail.com)  
[![GitHub](https://img.shields.io/badge/GitHub-black?logo=github)](https://github.com/sanyimo)  
[![Discord](https://img.shields.io/badge/Discord-blue?logo=discord)](https://discordapp.com/users/1300827475424837685)  

---

<br>

</details>

<details>
<summary>🇵🇹 Português</summary>

## 🍽️ O que é o GOO:D?

O **GOO:D** é uma plataforma web para compartilhar receitas, com suporte multilíngue, design responsivo e animações fluidas.  
Foi criada para oferecer uma experiência rica, visual e funcional tanto para usuários anônimos quanto para registrados.  

<br>

### 🚀 Tecnologias utilizadas

- **Backend:** Django  
- **Frontend:** JavaScript, SASS, AJAX  
- **Interfaces ricas:** Quill, Select2 (TinyMCE para administração)  
- **Tradução automática:** `LibreTranslate`  

<br>

### 👥 Características por tipo de utilizador

| Funcionalidade                                       | Visitantes (sem login) 👫 | Usuários registrados 🔐 |
|------------------------------------------------------|---------------------------|-------------------------|
| Visualizar receitas                                  | ✅                        | ✅                      |
| Busca avançada com filtros                           | ✅                        | ✅                      |
| Slider temático de receitas                          | ✅                        | ✅                      |
| Seção surpresa ("Não sabe o que cozinhar?")          | ✅                        | ✅                      |
| Salvar favoritos                                     | ❌                        | ✅                      |
| Comentar receitas                                    | ❌                        | ✅                      |
| Avaliar receitas                                     | ❌                        | ✅                      |
| Perfil com avatar e dados                            | ❌                        | ✅                      |
| Subir receitas (ser autor)                           | ❌                        | ✅                      |
| Editar / excluir próprias receitas                   | ❌                        | ✅ (apenas o autor)     |  

<br>

### 🛠️ Administração  
- Painel completo do Django Admin  
- Gestão de usuários, receitas, ingredientes, categorias etc.  
- Acesso exclusivo para superusuários  

<br>

### 🌍 Traduções automáticas

- As receitas criadas em um idioma são traduzidas automaticamente para os outros idiomas disponíveis.
- Para os textos da interface utiliza-se Django i18n, com suporte de Rosetta e Parler.
- Para os campos de texto livre, as traduções são geradas com LibreTranslate em produção.
- Além disso, foram realizadas mais de 2500 traduções manuais para garantir qualidade e naturalidade em todos os idiomas suportados.

<br>

### 🧾 Formulários detalhados  

O formulário de criação/edição de receitas permite:  

- Adicionar ingredientes de forma estruturada  
- Escrever passo a passo  
- Selecionar múltiplas categorias  
- Definir tags, alergênicos, nível de dificuldade, tipo de prato, tempo etc.  
- Usar tooltips nas tags como guia  

<br>

### 🎨 Interface e design  

| 🧩 **Bloco**                   | 📋 **Conteúdo**                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🌐 Geral                       | • Responsivo (mobile-first)<br>• Animações e microinterações cuidadosamente trabalhadas ✨<br>• Navegação criativa:<br>  🔄 Logotipo: prato giratório com toalha animada ao passar/clicar<br>  🍴 Utensílios como links, mesa posta como menu                                                                                                                                                                                                                                                 |
| 📑 Página de receitas          | • Top receitas: por média de avaliações ⭐<br>• Mais recentes: por data de publicação 🕒<br>• Favoritas: mais salvas pelos usuários 💖<br>• Fáceis: classificadas como “fáceis” 🥄<br>• Receitas da cozinha “xyz” (dinâmica): cozinha com mais receitas publicadas 🍲<br>• Receitas sazonais (dinâmicas): adaptadas ao calendário 🎉 (estações, feriados e eventos: Halloween 🎃, Natal 🎄, Ano Novo 🎆, Dia dos Namorados 💘, Carnaval 🎭, Dia das Mães 👩, Dia dos Pais 👨, Páscoa 🐣 etc.) |
| 👤 Seção especial “Meu Perfil” | • Design personalizado ✨<br>• Dividida em várias partes:<br>  📝 Dados pessoais: informações do usuário, alteração de avatar, email e senha<br>  📤 Minhas receitas publicadas<br>  💾 Favoritos: receitas marcadas como favoritas e salvas nesta seção<br>  💬 Comentários:<br>    – “meus comentários”<br>    – “respostas aos meus comentários”<br>    – “comentários nas minhas receitas”<br>  ⭐ Minhas avaliações: lista de receitas avaliadas pelo usuário                             |

<br>

### 📧 Extras  

- Formulário de contato com envio por email
- Sistema completo de login, registro e recuperação de senha via email  

> **Nota:** Este projeto foi desenvolvido para fins educacionais.  
> Os textos e imagens das receitas foram extraídos de [Comedera](https://comedera.com) e pertencem aos seus respectivos autores.  

<br>

## 🚀 Implantação  

O backend está implantado no **Alwaysdata**, integrado com o frontend e com suporte multilíngue.  
A tradução automática é feita por uma API externa em produção.  

👉 Acesse a aplicação:  
[https://goodgo.alwaysdata.net/](https://goodgo.alwaysdata.net/)

<br>

## 📫 Contato  

[![Email](https://img.shields.io/badge/Email-red?logo=gmail&logoColor=white)](mailto:sanyimo@gmail.com)  
[![GitHub](https://img.shields.io/badge/GitHub-black?logo=github)](https://github.com/sanyimo)  
[![Discord](https://img.shields.io/badge/Discord-blue?logo=discord)](https://discordapp.com/users/1300827475424837685)  

---

</details>
