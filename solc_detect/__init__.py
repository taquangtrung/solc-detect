
from semantic_version import NpmSpec, Version
from . import parser

# All Solidity releases: https://blog.soliditylang.org/category/releases/
solidity_0_4 = ['0.4.%d' % i for i in range(27)]      # 0.4.0 --> 0.4.26
solidity_0_5 = ['0.5.%d' % i for i in range(18)]      # 0.5.0 --> 0.5.17
solidity_0_6 = ['0.6.%d' % i for i in range(13)]      # 0.6.0 --> 0.6.12
solidity_0_7 = ['0.7.%d' % i for i in range(7)]       # 0.7.0 --> 0.7.6
solidity_0_8 = ['0.8.%d' % i for i in range(19)]      # 0.8.0 --> 0.8.19
all_solidity_versions = (solidity_0_4 +
                         solidity_0_5 +
                         solidity_0_6 +
                         solidity_0_7 +
                         solidity_0_8)


def find_solc_version(input_file):
    """Find the best version of Solc compiler for a smart contract."""
    pragma_version = parser.parse_solidity_version(input_file)
    version_spec = NpmSpec(pragma_version)
    all_versions = (Version(v) for v in all_solidity_versions)
    best_version = version_spec.select(all_versions)
    print("Best version: " + str(best_version))
    return best_version
