#!/usr/bin/perl -w

# carico le librerie
use strict;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use XML::LibXML;
use File::Copy;
use File::Basename; # serve per uploadare i file
use Time::localtime; # per conoscere la data corrente
use CGI::Pretty qw(:html3);
use URI;
use utf8;

# includo la mia libreria funzioni
require ('libreria_funzioni.pl');

# definisco la dimensione massima del file uploadato (5Mb)
$CGI::POST_MAX = 1024 * 5000;

# espressione regolare per il file immagine
my $file_er = "a-zA-Z0-9_.-";
my $upload_dir = "../img";

# creo oggetto cgi
my $cgi = new CGI;

my $filename = $cgi->param('img');
my $t = traduci($cgi->param('titolo'));
my $a = traduci($cgi->param('alt'));
my $c = traduci($cgi->param('contenuto'));
my $err_msg = "";
if (!trim($t) || !trim($a) || !trim($c))
{
# stampo pagina di errore
$err_msg = "uno o molteplici campi sono vuoti";
&errore($err_msg);
exit;
}
if(!$filename){
	# stampo pagina di errore
	$err_msg = "Il file è corrotto o supera la dimensione massima.";
	&errore($err_msg);
exit;
}

chomp $filename;
# faccio il parsing dell'immagine per estrarre il nome
my ($nome, $path, $estensione) = fileparse($filename, '\..*');

# controllo le estensioni del file
if (($estensione =~ /.png/i) || ($estensione =~ /.jpg/i) || ($estensione =~ /.jpeg/i) || ($estensione =~ /.gif/i)){
	# estensione valida
	$filename = $nome . $estensione;
	$filename =~ tr/ /_/;
	$filename =~ s/[^$file_er]//g;
	
	if($filename =~ /^([$file_er]+)$/){
		
		$filename = $1;
	}
	else{
		# stampo pagina di errore
		$err_msg = "Il nome del file contiene caratteri che non sono ammessi.";
		&errore($err_msg);
exit;
	}
	
	my $file_up = $cgi->upload("img");
	
	# carico l'immagine nella cartella img
	open (UPLOADFILE, ">../public_html/img/$filename") or die "$!";
	binmode UPLOADFILE;
	
	while( <$file_up> ){
		print UPLOADFILE;
	}
	close UPLOADFILE;
	
	# salvataggio della notizia in news.xml
	
	my $file = "../data/news.xml";

	# creazione oggetto parser
	my $parser = XML::LibXML->new();
	
	# apertura file e lettura input
	my $doc = $parser->parse_file($file);
	
	# estrazione radice
	my $root = $doc->getDocumentElement;
       
 my $id;
		my $path = $doc->findnodes("/news/notizia[last()]")->get_node(1);
if ($path){
		$id = $path->getAttribute('id');
}
else{
$id=0;
}
                my $notizia = XML::LibXML::Element->new('notizia');
		$notizia->setAttribute("id", $id+1); 


		my $imm = XML::LibXML::Element->new('img');
		$imm->appendText( "$upload_dir/$filename" );
		$notizia->appendChild($imm);
		
		my $alt = XML::LibXML::Element->new('alt');
		$alt->appendText( $a );
		$notizia->appendChild($alt);
                
                my $titolo = XML::LibXML::Element->new('titolo');
		$titolo->appendText( $t );
		$notizia->appendChild($titolo);
		my $datai = XML::LibXML::Element->new('datainserimento');
		# calcolo la data di adesso
		my $stime = localtime;
		my $Y = $stime->year+1900;
		my $M = $stime->mon+1;
		my $D = $stime->mday;
		my $dataoggi = "$Y-$M-$D";
		
		$datai->appendText( $dataoggi );
		$notizia->appendChild($datai);

                my $testo = XML::LibXML::Element->new('testocontenuto');
		$testo->appendText( $c );
		$notizia->appendChild($testo);
		
		
		
		$root->appendChild($notizia);
		
		# scrittura su file
		open(OUT,">$file") or die $!;
		print OUT $doc->toString;
		close(OUT);

	print "Content-type:text/html\n\n";
	print <<EOF;

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
	<title>Inserisci news-Judo Club Castelfranco Veneto</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <base href=""/>
      <link href="../css/Main.css" rel="stylesheet" type="text/css" media="screen"/>
        <link href="../css/print.css" rel="stylesheet" type="text/css" media="print"/>
<link rel="icon" type="image/png" href="../img/TaoIco.png"></link>
                <link href='http://fonts.googleapis.com/css?family=Shojumaru' rel='stylesheet' type='text/css'/>

    </head>
    <body>
		 		<div><a href="Home.cgi"><img class="tao" alt="tao" src="../img/TaoLogo.png"/></a><div class="titolo"><a href="Home.cgi"><span lang="en">Judo Club</span></a></div><div class="sottotitolo"><a href="Home.cgi">Castelfranco Veneto</a></div></div>
		                                		 <div class="menu">
            <ul class="lista-menu">
                <li><a href="Home.cgi"><span lang="en">HOME</span></a></li>
            <li><a href="../storia.html">STORIA CLUB</a></li>
            <li><a href="../ilJudo.html">IL <span lang="ja">JUDO</span></a></li>
            <li><a href="../ilBJJ.html">IL <span lang="ja">JIU JITSU</span> BRASILIANO</a></li>
            <li><a href="../maestri.html">MAESTRI</a></li>
            <li><a href="../orari.html">ORARI</a></li>
            <li><a href="info_contatti.cgi">INFO &amp; CONTATTI</a></li>
            </ul>		
        </div>
		
		<div class="navigazione">Sei qui: inserimento con successo</div>
		
        <div class="corpo">notizia inserita con successo, per inserirne altre torni alla <a href="./aggiungi_notizia.cgi">pagina di aggiunta notizie</a></div>
        
        <div class="footer"> <img class="valido" alt="css valido" src="../img/cssvalido.png"/><div class="indirizzo"> Via Boito, Castelfranco Veneto</div><img class="valido" alt="xhtml valido" src="../img/xhtmlvalido.png"/></div> <!-- mettere simboli w3c e html css valido-->
        
        
    </body>
</html>
EOF
}
else{
	# estensione non valida
	# stampo pagina di errore
	$err_msg = "L'estensione del file non è valida.";
	&errore($err_msg);
}
