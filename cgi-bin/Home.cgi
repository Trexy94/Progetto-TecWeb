#!/usr/bin/perl -w

# carico le librerie
use strict;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use XML::LibXML;
use File::Copy;
use utf8;
use URI;
use HTML::Parser;
use HTML::Entities;
# includo la mia libreria funzioni
require ('libreria_funzioni.pl');

my $session = CGI::Session->load();

my $auth;
if(!($session->is_expired) || !($session->is_empty)){
	# ricavo l'autenticazione
        $auth = $session->param('auth');
}
#basta controllare la stringa, perchè i non autenticati non hanno cookie e quindi dovrebbero conoscere la "magic word" e come è strutturato il login per craccarlo

# recupero dal file news.xml i dati della news con id corretto
my $file = "../data/news.xml";

# creazione oggetto parser
my $parser = XML::LibXML->new();

# apertura file e lettura input
my $doc = $parser->parse_file($file);


# stampo la HOME
print "Content-type:text/html\n\n";
print <<EOF;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
        <title>Home-Judo Club Castelfranco Veneto</title>
		<link rel="icon" type="image/png" href="../img/TaoIco.png"></link>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <base href=""/>
        <link href="../css/Main.css" rel="stylesheet" type="text/css" media="screen"/>
        <link href="../css/print.css" rel="stylesheet" type="text/css" media="print"/>
                <link href='http://fonts.googleapis.com/css?family=Shojumaru' rel='stylesheet' type='text/css'/>
				 <script type="text/javascript" src="../js/slide.js"></script>

    </head>
    <body onload="setUpSlideShow()">
		 		<div><img class="tao" alt="tao" src="../img/TaoLogo.png"/><div class="titolo"><span lang="en">Judo Club</span></div><div class="sottotitolo">Castelfranco Veneto</div></div>
		 <div class="menu">
            <ul class="lista-menu">
            <li class="attivo"><span lang="en">HOME</span></li>
            <li><a href="../storia.html">STORIA CLUB</a></li>
            <li><a href="../ilJudo.html">IL <span lang="ja">JUDO</span></a></li>
            <li><a href="../ilBJJ.html">IL <span lang="ja">JIU JITSU</span> BRASILIANO</a></li>
            <li><a href="../maestri.html">MAESTRI</a></li>
            <li><a href="../orari.html">ORARI</a></li>
            <li><a href="info_contatti.cgi">INFO &amp; CONTATTI</a></li>
            </ul>		
        </div>
					<div id="slideshow">
                         <div id="slides">
                             <div class="slide">
                                 <img src="../img/Slide1.jpg" alt="immagini varie della palestra"/></div>
                             <div class="slide">
                                 <img src="../img/Slide2.jpg" alt="immagini varie della palestra"/></div>
                             <div class="slide">
                                 <img src="../img/Slide3.jpg" alt="immagini varie della palestra"/></div>
							 <div class="slide">
                                 <img src="../img/Slide4.jpg" alt="immagini varie della palestra"/></div>
                         </div>
<div id="slides-controls"></div>
                     </div>

					 <div class="navigazione">Sei qui: Home</div>
	 <h2 class="testo_posizionato">Ultime notizie:</h2>
		
EOF

#aggiunta notizie per amministratore
if($auth eq "amministratoreautenticato"){
print "<h3><a href=\"./aggiungi_notizia.cgi\">aggiungi notizia</a></h3>";
}
# estrazione delle news
my @news = $doc->findnodes("/news/notizia");
@news=reverse(@news);
#per avere le news dalla più recente alla più vecchia
# stampa delle news
foreach my $notizia (@news){
	my $img = $notizia->findvalue('img');
        my $alt = decode_entities($notizia->findvalue('alt'));
	my $titolo = decode_entities($notizia->findvalue('titolo'));
	my $data = $notizia->findvalue('datainserimento');
        my $id = $notizia->getAttribute('id');
		print "<div class= \"news\">
				<div class=\"data_news\">Scritto il : <strong>$data</strong></div>
                  <a href=\"viss_news.cgi?id=$id\" class=\"immagine_link\"><img src=\"$img\" alt=\"$alt\" class=\"immagine_news\"/></a>
				<p class=\"titolo_news\"><a href=\"viss_news.cgi?id=$id\" class=\"titolo_news\">$titolo</a></p>";

	if($auth eq "amministratoreautenticato"){
		# stampo il bottone per eliminare la notizia
		
                                print "<form action=\"elimina_notizia.cgi\" class=\"elimina_notizia\" method=\"post\">
                                            <p>
						<input type=\"hidden\" name=\"notizia\" value=\"$id\"/>
						<input type=\"submit\" name=\"elimina\" value=\"Elimina\"/>
                                            </p>
					</form>";
	}
print '</div>';
}
print '<div class="footer"> <img class="valido" alt="css valido" src="../img/cssvalido.png"/><div class="indirizzo"> Via Boito, Castelfranco Veneto</div><a href="./amministratore.cgi">Amministrazione</a><img class="valido" alt="xhtml valido" src="../img/xhtmlvalido.png"/></div> <!-- mettere simboli w3c e html css valido-->
    </body>
</html>';
