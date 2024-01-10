"use client"

import Image from "next/image"
import * as logo from '@/static/logo2.png';
import * as settings from '@/static/settings.png';
import styles from './header.module.css'

const Header = () => {
  return (
    <header className={styles.header}>

      <Image src={logo} alt={"dev logo"} width={122} height={24}/>
      <input type="Поиск" placeholder="Поиск" className={styles.search}/>
      <div className={styles.profile}>
        <div className={styles.settings}>
        <Image src={settings} alt={"dev logo"} width={24} height={24}/>
        </div>
        <div>Профиль</div>
      </div>
    </header>

  )
}

export default Header
