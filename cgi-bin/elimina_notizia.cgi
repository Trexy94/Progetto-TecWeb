#!/usr/bin/perl -w

# carico le librerie
use strict;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session;
use CGI::Cookie;
use XML::LibXML;
use XML::LibXSLT;
use File::Copy;
use POSIX;
use URI;

# includo la mia libreria funzioni
require ('libreria_funzioni.pl');

# leggo i dati dal POST e li inserisco nell'hash DATI
my %DATI = &leggi_post();	
	
			if(!%DATI){
				# in caso l'admin carichi la pagina da url
				print redirect($ENV{HTTP_REFERER});
			}
			# Carico file utenti.xml
			my $file = "../data/news.xml";
		
			# creazione oggetto parser
			my $parser = XML::LibXML->new();
		
			# apertura file e lettura input
			my $doc = $parser->parse_file($file);
			
			# estraggo dal l'id della notizia da eliminare
			my $id = $DATI{'notizia'};
						
			# mi posiziono sul nodo da eliminare
			my $node = $doc->findnodes("/news/notizia[\@\id = $id]")->get_node(1);
			
			# trovo il padre
			my $parent = $node->parentNode;
			# elimino il nodo
			$parent->removeChild($node);
			
			# stampo modifiche
			# scrittura su file
			open(OUT,">$file") or die $!;
			print OUT $doc->toString;
			close(OUT);
			
			print "Location:Home.cgi\n\n";
			
			
