#define SOCKET_STATE_READY			0
#define SOCKET_STATE_BIND_REQ		1
#define SOCKET_STATE_CONNECT_REQ	2
#define SOCKET_STATE_BOUND			3
#define SOCKET_STATE_LISTEN_REQ		4
#define SOCKET_STATE_LISTENING		5
#define SOCKET_STATE_OPEN			6
#define SOCKET_STATE_CLOSE_REQ		7
#define SOCKET_STATE_CLOSED			8

#define SOCKET_STREAM	1
#define SOCKET_DATAGRAM	2
#define SOCKET_RAW		3

#define AF_UNSPEC	0
#define	AF_INET		2
#define AF_INET6	10

#define INADDR_ANY	0

#define INET_ADDRSTRLEN		16 //pubs.opengroup.com netinit/in.h
#define INET6_ADDRSTRLEN	46

#define INET_MIN_ADDRSTRLEN		7 // ex: len of 0.0.0.0
#define INET6_MIN_ADDRSTRLEN	2 // ie: len of ::


#define IP_PARSE_STATE_NUM			0
#define IP_PARSE_STATE_DOT			1

class CIPV4Address
{
	U32 address;	// 'in Network Byte order' ... Big Endian
};

class CIPV6Address
{
	U8	address[16]; // a clear #define would be nice
};

class CIPAddressStorage
{// class specifically meant to be generic casted either IPV4 or IPV6 Address.
	U8	padding[16];
};

class CSocketAddressIPV4
{
	U16				family;		// 'AF_INET'
	U16				port;		// 'in Network Byte order' ... Big Endian
	CIPV4Address	address;
	U8				zeroes[8];	// 'same size as socket address'
};

class CSocketAddressIPV6
{
	U16				family;	// 'AF_INET6'
	U16				port;	// 'in Network Byte order'... Big Endian
	U32				flow_info;
	CIPV6Address	address;
	U32				scope_id;
};

class CSocketAddressStorage
{/*	'designed to be large enough to
	hold both IPV4 and IPV6 structures.' */

	U16 family;
	U8	padding[26];
};

class CAddressInfo
{
	I32						 flags;
	I32						 family;
	I32						 socket_type;
	I32						 protocol;
	I64						 address_length;
	CSocketAddressStorage	*address;
	U8						*canonical_name;
	CAddressInfo			*next;
};

class CSocket
{
	U8	state;

	U16	type;
	U16 domain;
};
