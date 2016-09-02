from codec import Choice, Enumerated, Map, Record, VBoolean, VInteger, VString

"""
Cyber Observable Expression v3.0 (cybox) definitions used by OpenC2
"""

# Core vocabularies

class HashAlgorithmType(Enumerated):    # Cybox 3.0 does not define a TypeName
    ns = 'cybox3'                       # Open vocabulary, Type string is 'hash-algo-ov'
    vals = [            # ElementID:
        'md5',              #  1
        'md6',              #  2
        'ripemd-160',       #  3
        'sha-1',            #  4
        'sha-224',          #  5
        'sha-256',          #  6
        'sha-384',          #  7
        'sha-512',          #  8
        'sha3-224',         #  9
        'sha3-256',         # 10
        'sha3-384',         # 11
        'sha3-512',         # 12
        'ssdeep',           # 13
        'whirlpool'         # 14
    ]

class EncryptionAlgorithmType(Enumerated):
    ns = 'cybox3'                       # Open vocabulary, Type string is 'encryption-algo-ov'
    vals = [                # ElementID:
        'aes128-ecb',           #  1
        'aes128-cbc',           #  2
        'aes128-cfb',           #  3
        'aes128-cofb',          #  4
        'aes128-ctr',           #  5
        'aes128-xts',           #  6
        'aes128-gcm',           #  7
        'salsa20',              #  8
        'salsa8',               #  9
        'chacha20-poly1305',    # 10
        'chacha20',             # 11
        'des-cbc',              # 12
        '3des-cbc',             # 13
        'des-ebc',              # 14
        '3des-ebc',             # 15
        'cast128-cbc',          # 16
        'cast256-cbc'           # 17
    ]

# Host Objects

class FileObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', VString, ''),      # Must be 'file-object'
        ('description', VString, '?'),
        ('extended_properties', FileExtensions, '?'),
        ('hashes', Hashes, '?'),    # Dictionary of hashes
        ('size', VInteger, '?'),
        ('file_name', VString, '?'),
        ('file_name_enc', VString, '?'),
        ('file_name_hex', VString, '?'),    # hex
        ('magic_number', VString, '?'),     # hex
        ('mime_type', VString, '?'),
        ('created', VString, '?'),          # timestamp
        ('modified', VString, '?'),         # timestamp
        ('accessed', VString, '?'),         # timestamp
        ('parent_directory_ref', VString, '?'), # object-ref to directory-object
        ('is_encrypted', VBoolean, '?'),
        ('encryption_algorithm', EncryptionAlgorithmType, '?'),     # is_encrypted MUST be True
        ('decryption_key', VString, '?'),   # is_encrypted MUST be True
        ('contains_refs', CyboxObjectRefs, '?'),    # list of object-ref
        ('file_content_ref', ArtifactObjectRef, '?')    # artifact-object
    ]

class DirectoryObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', VString, ''),      # Must be 'directory-object'
        ('description', VString, '?'),
        ('extended_properties', FileExtensions, '?'),
        ('path', VString, ''),
        ('path_enc', VString, '?'),
        ('path_hex', VString, '?'),         # hex
        ('created', VString, '?'),  # timestamp
        ('modified', VString, '?'),  # timestamp
        ('accessed', VString, '?'),  # timestamp
        ('contains_refs', ObjectRefs, '?'),  # list of object-ref to file-object or directory-object
    ]

class WindowsRegistryKeyObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', VString, ''),      # Must be 'windows-registry-key-object'
        ('description', VString, '?'),
        ('extended_properties', FileExtensions, '?'),
        ('key', VString, ''),
        ('values', WindowsRegistryValueTypes, '?'),
        ('modified', VString, '?'),         # timestamp
        ('creator_ref', ObjectRef, '?'),    # object-ref to user-account-object
        ('number_of_subkeys', VInteger, '?')
    ]

class MutexObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', VString, ''),      # Must be 'mutex-object'
        ('description', VString, '?'),
        ('extended_properties', FileExtensions, '?'),
        ('name', VString, '')
    ]

#  x509-certificate-object
#  software-object
#  artifact-object
#  process-object
#  user-account-object

# Network Objects

class IPv4AddressObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', VString, ''),                      # Must be 'ipv4-address-object'
        ('description', VString, '?'),
        ('extended_properties', FileExtensions, '?'),
        ('value', VString, ''),                     # CIDR format
        ('resolves_to_refs', ObjectRefs, '?'),      # list of object-ref to mac-address-object
        ('belongs_to_refs', ObjectRefs, '?')        # list of object ref to as-object
    ]

class IPv6AddressObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', VString, ''),                      # Must be 'ipv6-address-object'
        ('description', VString, '?'),
        ('extended_properties', FileExtensions, '?'),
        ('value', VString, ''),                     # CIDR format
        ('resolves_to_refs', ObjectRefs, '?'),      # list of object-ref to mac-address-object
        ('belongs_to_refs', ObjectRefs, '?')        # list of object ref to as-object
    ]

class MACAddressObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', VString, ''),              # Must be 'mac-address-object'
        ('description', VString, '?'),
        ('extended_properties', FileExtensions, '?'),
        ('value', VString, ''),             # colon-delimited MAC-48 address
    ]

class EmailAddressObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', VString, ''),              # Must be 'email-address-object'
        ('description', VString, '?'),
        ('extended_properties', FileExtensions, '?'),
        ('value', VString, ''),             # RFC 5322 addr-spec
        ('display_name', VString, '?')      # RFC 5322 display-name
    ]

class URLObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', VString, ''),              # Must be 'url-object'
        ('description', VString, '?'),
        ('extended_properties', FileExtensions, '?'),
        ('value', VString, '')
    ]

class DomainNameObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', VString, ''),              # Must be 'domain-name-object'
        ('description', VString, '?'),
        ('extended_properties', FileExtensions, '?'),
        ('value', VString, ''),
        ('resolves_to_refs', ObjectRefs, '?'),  # list of object-ref to ipv4-address-object, ipv6-address-object, domain-name-object
    ]                                           #  Typo - called resolves-to as of 8/30

class ASObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', VString, ''),      # Must be 'as-object'
        ('description', VString, '?'),
        ('extended_properties', FileExtensions, '?'),
        ('number', VInteger, ''),
        ('name', VString, '?'),
        ('regional_internet_Registry', VString, '?')
    ]

#  Network Connection Object
#  Email Message Object

# Common Types

class CyboxObject(Choice):
    ns = 'cybox3'
    vals = [
        ('')
    ]

class CyboxBaseObject(Record):              # Base type for all CybOX 3 objects
    ns = 'cybox3'                           # TODO: combine vals instead of replacing in derived class
    vals = [
        ('type', CyboxObjects, ''),
        ('description', VString, '?'),
        ('extended_properties', Map, '?')
    ]

class CyboxContainer(Record):           # Collection of related CybOX 3 objects and actions
    ns = 'cybox3'
    vals = [
        ('type', VString, ''),          # 'cybox-container'
        ('spec_version', VString, ''),  #  e.g., '3.0'
        ('objects', CyboxObjects, '?'), # Cybox 3.0 says 'dictionary' with list index properties, allow real list
        ('actions', CyboxActions, '?')  # RESERVED
    ]
