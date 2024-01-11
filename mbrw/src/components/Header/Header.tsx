"use client"

import Image from "next/image"
import * as logo from '@/static/logo2.png';
import * as settings from '@/static/settings.png';
import * as search from '@/static/search.png';
import styles from './header.module.css'
import Link from "next/link";
import { Montserrat } from 'next/font/google'


const montserrat = Montserrat({ subsets: ['latin'] })

const Header = () => {
  return (
    <header className={styles.header}>
      <Link href={"/"}>
        <Image src={logo} alt={"dev logo"} width={122} height={24} />
      </Link>
      <div className={styles.container}>
        <input type="Поиск" placeholder="Поиск" className={styles.search} />
          <Image src={search} alt={"dev logo"} width={18} height={18} />


      </div>
      <div className={styles.profile}>
        <Link href={"/settings"}>
          <div className={styles.settings}>
            <Image src={settings} alt={"dev logo"} width={24} height={24} />
          </div>
        </Link>
        <div>Профиль</div>
      </div>
    </header>

  )
}

export default Header
