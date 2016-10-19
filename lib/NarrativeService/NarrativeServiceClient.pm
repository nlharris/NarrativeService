package NarrativeService::NarrativeServiceClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

NarrativeService::NarrativeServiceClient

=head1 DESCRIPTION


A KBase module: NarrativeService


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => NarrativeService::NarrativeServiceClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my $token = Bio::KBase::AuthToken->new(@args);
	
	if (!$token->error_message)
	{
	    $self->{token} = $token->token;
	    $self->{client}->{token} = $token->token;
	}
        else
        {
	    #
	    # All methods in this module require authentication. In this case, if we
	    # don't have a token, we can't continue.
	    #
	    die "Authentication failed: " . $token->error_message;
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 list_objects_with_sets

  $return = $obj->list_objects_with_sets($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a NarrativeService.ListObjectsWithSetsParams
$return is a NarrativeService.ListObjectsWithSetsOutput
ListObjectsWithSetsParams is a reference to a hash where the following keys are defined:
	ws_name has a value which is a string
	ws_id has a value which is an int
ListObjectsWithSetsOutput is a reference to a hash where the following keys are defined:
	data has a value which is a reference to a list where each element is a NarrativeService.ListItem
ListItem is a reference to a hash where the following keys are defined:
	object_info has a value which is a NarrativeService.object_info
	set_items has a value which is a NarrativeService.SetItems
object_info is a reference to a list containing 11 items:
	0: (objid) an int
	1: (name) a string
	2: (type) a string
	3: (save_date) a NarrativeService.timestamp
	4: (version) an int
	5: (saved_by) a string
	6: (wsid) an int
	7: (workspace) a string
	8: (chsum) a string
	9: (size) an int
	10: (meta) a reference to a hash where the key is a string and the value is a string
timestamp is a string
SetItems is a reference to a hash where the following keys are defined:
	set_items_info has a value which is a reference to a list where each element is a NarrativeService.object_info

</pre>

=end html

=begin text

$params is a NarrativeService.ListObjectsWithSetsParams
$return is a NarrativeService.ListObjectsWithSetsOutput
ListObjectsWithSetsParams is a reference to a hash where the following keys are defined:
	ws_name has a value which is a string
	ws_id has a value which is an int
ListObjectsWithSetsOutput is a reference to a hash where the following keys are defined:
	data has a value which is a reference to a list where each element is a NarrativeService.ListItem
ListItem is a reference to a hash where the following keys are defined:
	object_info has a value which is a NarrativeService.object_info
	set_items has a value which is a NarrativeService.SetItems
object_info is a reference to a list containing 11 items:
	0: (objid) an int
	1: (name) a string
	2: (type) a string
	3: (save_date) a NarrativeService.timestamp
	4: (version) an int
	5: (saved_by) a string
	6: (wsid) an int
	7: (workspace) a string
	8: (chsum) a string
	9: (size) an int
	10: (meta) a reference to a hash where the key is a string and the value is a string
timestamp is a string
SetItems is a reference to a hash where the following keys are defined:
	set_items_info has a value which is a reference to a list where each element is a NarrativeService.object_info


=end text

=item Description



=back

=cut

 sub list_objects_with_sets
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function list_objects_with_sets (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to list_objects_with_sets:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'list_objects_with_sets');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "NarrativeService.list_objects_with_sets",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'list_objects_with_sets',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method list_objects_with_sets",
					    status_line => $self->{client}->status_line,
					    method_name => 'list_objects_with_sets',
				       );
    }
}
 


=head2 copy_narrative

  $return = $obj->copy_narrative($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a NarrativeService.CopyNarrativeParams
$return is a NarrativeService.CopyNarrativeOutput
CopyNarrativeParams is a reference to a hash where the following keys are defined:
	workspaceRef has a value which is a string
	workspaceId has a value which is an int
	newName has a value which is a string
CopyNarrativeOutput is a reference to a hash where the following keys are defined:
	newWsId has a value which is an int
	newNarId has a value which is an int

</pre>

=end html

=begin text

$params is a NarrativeService.CopyNarrativeParams
$return is a NarrativeService.CopyNarrativeOutput
CopyNarrativeParams is a reference to a hash where the following keys are defined:
	workspaceRef has a value which is a string
	workspaceId has a value which is an int
	newName has a value which is a string
CopyNarrativeOutput is a reference to a hash where the following keys are defined:
	newWsId has a value which is an int
	newNarId has a value which is an int


=end text

=item Description



=back

=cut

 sub copy_narrative
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function copy_narrative (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to copy_narrative:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'copy_narrative');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "NarrativeService.copy_narrative",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'copy_narrative',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method copy_narrative",
					    status_line => $self->{client}->status_line,
					    method_name => 'copy_narrative',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "NarrativeService.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "NarrativeService.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'copy_narrative',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method copy_narrative",
            status_line => $self->{client}->status_line,
            method_name => 'copy_narrative',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for NarrativeService::NarrativeServiceClient\n";
    }
    if ($sMajor == 0) {
        warn "NarrativeService::NarrativeServiceClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 timestamp

=over 4



=item Description

A time in the format YYYY-MM-DDThh:mm:ssZ, where Z is either the
character Z (representing the UTC timezone) or the difference
in time to UTC in the format +/-HHMM, eg:
    2012-12-17T23:24:06-0500 (EST time)
    2013-04-03T08:56:32+0000 (UTC time)
    2013-04-03T08:56:32Z (UTC time)


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 permission

=over 4



=item Description

Represents the permissions a user or users have to a workspace:

'a' - administrator. All operations allowed.
'w' - read/write.
'r' - read.
'n' - no permissions.


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 lock_status

=over 4



=item Description

The lock status of a workspace.
One of 'unlocked', 'locked', or 'published'.


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 object_info

=over 4



=item Description

Information about an object, including user provided metadata.

obj_id objid - the numerical id of the object.
obj_name name - the name of the object.
type_string type - the type of the object.
timestamp save_date - the save date of the object.
obj_ver ver - the version of the object.
username saved_by - the user that saved or copied the object.
ws_id wsid - the workspace containing the object.
ws_name workspace - the workspace containing the object.
string chsum - the md5 checksum of the object.
int size - the size of the object in bytes.
usermeta meta - arbitrary user-supplied metadata about
    the object.


=item Definition

=begin html

<pre>
a reference to a list containing 11 items:
0: (objid) an int
1: (name) a string
2: (type) a string
3: (save_date) a NarrativeService.timestamp
4: (version) an int
5: (saved_by) a string
6: (wsid) an int
7: (workspace) a string
8: (chsum) a string
9: (size) an int
10: (meta) a reference to a hash where the key is a string and the value is a string

</pre>

=end html

=begin text

a reference to a list containing 11 items:
0: (objid) an int
1: (name) a string
2: (type) a string
3: (save_date) a NarrativeService.timestamp
4: (version) an int
5: (saved_by) a string
6: (wsid) an int
7: (workspace) a string
8: (chsum) a string
9: (size) an int
10: (meta) a reference to a hash where the key is a string and the value is a string


=end text

=back



=head2 SetItems

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
set_items_info has a value which is a reference to a list where each element is a NarrativeService.object_info

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
set_items_info has a value which is a reference to a list where each element is a NarrativeService.object_info


=end text

=back



=head2 ListItem

=over 4



=item Description

object_info - workspace info for object (including set object),
set_items - optional property listing info for items of set object


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
object_info has a value which is a NarrativeService.object_info
set_items has a value which is a NarrativeService.SetItems

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
object_info has a value which is a NarrativeService.object_info
set_items has a value which is a NarrativeService.SetItems


=end text

=back



=head2 ListObjectsWithSetsParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
ws_name has a value which is a string
ws_id has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
ws_name has a value which is a string
ws_id has a value which is an int


=end text

=back



=head2 ListObjectsWithSetsOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
data has a value which is a reference to a list where each element is a NarrativeService.ListItem

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
data has a value which is a reference to a list where each element is a NarrativeService.ListItem


=end text

=back



=head2 CopyNarrativeParams

=over 4



=item Description

workspaceId - optional workspace ID, if not specified then 
    property from workspaceRef object info is used.


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspaceRef has a value which is a string
workspaceId has a value which is an int
newName has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspaceRef has a value which is a string
workspaceId has a value which is an int
newName has a value which is a string


=end text

=back



=head2 CopyNarrativeOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
newWsId has a value which is an int
newNarId has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
newWsId has a value which is an int
newNarId has a value which is an int


=end text

=back



=cut

package NarrativeService::NarrativeServiceClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
