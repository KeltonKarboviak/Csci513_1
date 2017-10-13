#!/usr/bin/perl

use strict;
use CGI;

my $query = new CGI;
my $username = $query->param('cust_username');

# Remove leading and trailing spacing
$username =~ s/^\s+|\s+$//g;

# For security, remove some Unix metacharacters
# $name =~ s/;|>|>>|<|\*|\?|\&|\|//g;
$username =~ s/"/\\"/g;

# Compose a Java command
my $cmd = "/usr/bin/java -Djava.security.egd=file:/dev/./urandom CustSignin \"$username\"";

system($cmd);
