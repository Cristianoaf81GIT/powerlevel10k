#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"
  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  P9K_HOME=$(pwd)
  ### Test specific
  # Create default folder and git init it.
  FOLDER=/tmp/powerlevel9k-test
  mkdir -p "${FOLDER}"
  cd $FOLDER
}

function tearDown() {
  # Go back to powerlevel9k folder
  cd "${P9K_HOME}"
  # Remove eventually created test-specific folder
  rm -fr "${FOLDER}"
  # At least remove test folder completely
  rm -fr /tmp/powerlevel9k-test
}

function testSymfonyVersionSegmentPrintsNothingIfPhpIsNotAvailable() {
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(symfony2_version custom_world)
    local POWERLEVEL9K_CUSTOM_WORLD='echo world'
    alias php="nophp"

    assertEquals "%K{white} %F{black}world %k%F{white}%f " "$(build_left_prompt)"

    unalias php
}

function testSymfonyVersionSegmentPrintsNothingIfSymfonyIsNotAvailable() {
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(symfony2_version custom_world)
    # "Symfony" is not a command, but rather a framework.
    # To sucessfully execute this test, we just need to
    # navigate into a folder that does not contain symfony.
    local POWERLEVEL9K_CUSTOM_WORLD='echo world'

    assertEquals "%K{white} %F{black}world %k%F{white}%f " "$(build_left_prompt)"
}

function testSymfonyVersionPrintsNothingIfPhpThrowsAnError() {
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(symfony2_version custom_world)
    local POWERLEVEL9K_CUSTOM_WORLD='echo world'
    mkdir app
    touch app/AppKernel.php
    function php() {
        echo "Warning: Unsupported declare strict_types in /Users/dr/Privat/vendor/ocramius/proxy-manager/src/ProxyManager/Configuration.php on line 19

        Parse error: parse error, expecting `;´ or `{´ in /Users/dr/Privat/vendor/ocramius/proxy-manager/src/ProxyManager/Configuration.php on line 97"
    }

    assertEquals "%K{white} %F{black}world %k%F{white}%f " "$(build_left_prompt)"

    unfunction php
}

function testSymfonyVersionSegmentWorks() {
    startSkipping # Skip test
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(symfony2_version)
    mkdir app
    touch app/AppKernel.php

    function php() {
        echo "Symfony version 3.1.4 - app/dev/debug"
    }

    assertEquals "%K{240} %F{black%}SF %f%F{black}3.1.4 %k%F{240}%f " "$(build_left_prompt)"

    unfunction php
}

function testSymfonyVersionSegmentWorksInNestedFolder() {
    startSkipping # Skip test
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(symfony2_version)
    mkdir app
    touch app/AppKernel.php

    function php() {
        echo "Symfony version 3.1.4 - app/dev/debug"
    }

    mkdir -p src/P9K/AppBundle
    cd src/P9K/AppBundle

    assertEquals "%K{240} %F{black%}SF %f%F{black}3.1.4 %k%F{240}%f " "$(build_left_prompt)"

    unfunction php
}

source shunit2/source/2.1/src/shunit2