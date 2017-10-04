#!/usr/bin/perl

use CGI;
$query   = new CGI;
# $act     = $query->param('act');
$name = $query->param('name');

# Remove leading and trailing spacing.
$name =~ s/^\s+|\s+$//g;

# For security, remove some Unix metacharacters.
# $name =~ s/;|>|>>|<|\*|\?|\&|\|//g;
$name =~ s/"/\\"/g

# Compose a Java command.
$cmd    =  "/usr/bin/java -Djava.security.egd=file:/dev/./urandom AddDeveloper \"$name\"";
system($cmd);
