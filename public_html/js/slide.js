slidePrefix            = "slide-";
slideControlPrefix     = "slide-control-";
slideHighlightClass    = "highlight";
slidesContainerID      = "slides";
slidesControlsID       = "slides-controls";
slideDelay             = 3000;

function setUpSlideShow()
{
    //faccio comparire i pulsanti di navigazione
document.getElementById("slides-controls").innerHTML='<a href="#">1</a><a href="#">2</a><a href="#">3</a><a href="#">4</a>';
    // recupera le slide e i controlli
    slidesCollection = document.getElementById(slidesContainerID).children;
    slidesControllersCollection = document.getElementById(slidesControlsID).children;
 
    totalSlides = slidesCollection.length;
 
    if (totalSlides < 2) return;
 
    //ciclo le slide
    for (var i=0; i < slidesCollection.length; i++)
    {
        // do l'id alle slide e ai controlli
        slidesCollection[i].id = slidePrefix+(i+1);
        slidesControllersCollection[i].id = slideControlPrefix+(i+1);
 
        // collego i pulsanti con l'azione che faranno
        slidesControllersCollection[i].onclick = function(){clickSlide(this);};
 
        //nascondo tutte le slide tranne la prima
        if (i > 0)
            slidesCollection[i].style.display = "none";
        else
            slidesControllersCollection[i].className = slideHighlightClass;
    }
 
    // inizializzo le variabili
    transTimeout  = 0;
    crtSlideIndex = 1;
 
    // mostro la slide successiva
    showSlide(2);
}

function showSlide(slideNo, immediate)
{
	// non permetto azioni durante la transizione
    if (slideNo === crtSlideIndex)
        return;
 
    clearTimeout(transTimeout);
 
	// prendo la slide attuale e la successiva
    nextSlideIndex = slideNo;
    crtSlide = document.getElementById(slidePrefix + crtSlideIndex);
    nextSlide = document.getElementById(slidePrefix + nextSlideIndex);
 
    // setto la transizione sia con pulsante sia con timeout
    if (immediate === true)
        transSlide();
    else
        transTimeout = setTimeout("transSlide()", slideDelay);
}

function clickSlide(control)
{
    showSlide(Number(control.id.substr(control.id.lastIndexOf("-")+1)),true);
}


 
function transSlide()
{
    nextSlide.style.display = "block";
        // passo alla prossima slide
        crtSlide.style.display = "none";
        transComplete();
    }

function transComplete()
{
    crtSlideIndex = nextSlideIndex;
 
    // mostro la slide successiva
    showSlide((crtSlideIndex >= totalSlides) ? 1 : crtSlideIndex + 1);
 
    //deevidenzio i controlli
    for (var i=0; i < slidesControllersCollection.length; i++)
        slidesControllersCollection[i].className = "";
 
    // evidenzio il corretto controllo
    document.getElementById("slide-control-" + crtSlideIndex).className = slideHighlightClass;
}
