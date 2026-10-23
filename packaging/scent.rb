# PREPARED, NOT PUBLISHED. Shape: lope bc388673 packaging/lope.rb.
# Source build from a future tag; no dependency on a moving wolf formula.
class Scent < Formula
  desc "Byte-oriented grep in wolf with basic, extended and fixed patterns"
  homepage "https://github.com/wolffe-lang/scent"
  url "https://github.com/wolffe-lang/scent/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "RELEASE-LANE-FILLS-THIS"
  license "GPL-3.0-or-later"
  depends_on "llvm" => :build

  resource "wolf" do
    on_macos do
      on_arm do
        url "https://github.com/wolffe-lang/wolf-lang/releases/download/v0.2.35/wolf-0.2.35-aarch64-apple-darwin.tar.gz"
        sha256 "240b84d079b1b9a0d88681ac08fca4816f84778e2d6c94c435ceb2dd6a5f042a"
      end
    end
    on_linux do
      on_intel do
        url "https://github.com/wolffe-lang/wolf-lang/releases/download/v0.2.35/wolf-0.2.35-x86_64-unknown-linux-gnu.tar.gz"
        sha256 "4cc4045bbbb605c07835bc4f32685953c784eeef4cd3139a48b457dfc90dad1a"
      end
    end
  end

  def install
    source = buildpath
    resource("wolf").stage do
      odie "bundled std pin drift" unless (Pathname.pwd/"std/STD-REV").read.strip == "2386522eb059cca5a84108562c2c0a0e72345d34"
      ENV["WOLF_STD"] = (Pathname.pwd/"std").to_s
      system "./wolf", "build", "--release", "--deny-warnings", source/"src/scent.lu", "-o", source/"scent"
    end
    bin.install "scent"
    (libexec/"gnubin").install_symlink bin/"scent" => "grep"
    (libexec/"gnubin").install "wrappers/egrep", "wrappers/fgrep"
    doc.install "README.md", "CHANGELOG.md"
  end

  def caveats
    "Optional grep/egrep/fgrep names are in #{libexec}/gnubin. They do not replace the system grep."
  end

  test do
    assert_equal "ab\n", pipe_output("#{bin}/scent -E '^a[ab]$'", "ab\nno\n", 0)
    assert_equal "aa\n", pipe_output("#{bin}/scent -G '\\(a\\)\\1'", "aa\nno\n", 0)
    assert_match "scent #{version}", shell_output("#{bin}/scent --version")
  end
end
